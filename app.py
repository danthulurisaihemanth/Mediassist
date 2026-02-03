from flask import Flask, render_template, request, jsonify, session
from core.langgraph_workflow import setup_workflow
from core.state import initialize_state
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

workflow = setup_workflow()

@app.route('/')
def home():
    session['conversation_id'] = datetime.now().strftime("%Y%m%d%H%M%S")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    language = request.json.get('language', 'en')  # Get selected language, default to English
    conversation_state = initialize_state()
    
    if 'history' not in session:
        session['history'] = []
    
    session['history'].append(f"User: {user_input}")
    
    # Include language in the conversation state
    conversation_state.update({
        "question": user_input,
        "language": language,  # Pass language to LLM
        "conversation_history": session['history']
    })
    
    # LLM workflow invocation
    result = workflow.invoke(conversation_state)
    bot_response = result.get('generation', "I couldn't generate a response.")
    
    # Update session with the current language (in case it changed)
    session['current_language'] = result.get('language', language)
    
    session['history'].append(f"Doctor: {bot_response}")
    
    return jsonify({
        'response': bot_response,
        'timestamp': datetime.now().strftime("%H:%M"),
        'language': result.get('language', language)  # Return current language
    })


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Respond to WhatsApp messages via Twilio."""
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    # Create a unique session per sender
    if 'wa_history' not in session:
        session['wa_history'] = {}

    if sender not in session['wa_history']:
        session['wa_history'][sender] = []

    conversation_state = initialize_state()
    conversation_state.update({
        "question": incoming_msg,
        "language": "auto",
        "conversation_history": session['wa_history'][sender]
    })

    result = workflow.invoke(conversation_state)
    bot_response = result.get("generation", "Sorry, I couldn't understand that.")

    # Update conversation history for this sender
    session['wa_history'][sender].append(f"User: {incoming_msg}")
    session['wa_history'][sender].append(f"Doctor: {bot_response}")

    # Create Twilio response
    resp = MessagingResponse()
    resp.message(bot_response)
    return str(resp)


@app.route('/accuracy', methods=['GET'])
def get_accuracy():
    """Get latest accuracy metrics"""
    try:
        # Try to load latest evaluation results
        import glob
        result_files = glob.glob('evaluation_results_*.json')
        if result_files:
            latest_file = max(result_files, key=os.path.getctime)
            with open(latest_file, 'r') as f:
                results = json.load(f)
            return jsonify({
                'success': True,
                'accuracy': results['average_accuracy'],
                'total_tests': results['total_tests'],
                'timestamp': results['timestamp'],
                'by_difficulty': results['accuracy_by_difficulty'],
                'by_category': results['accuracy_by_category']
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No evaluation results found. Run evaluation first.'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/accuracy-dashboard')
def accuracy_dashboard():
    """Display accuracy dashboard"""
    return render_template('accuracy_dashboard.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
