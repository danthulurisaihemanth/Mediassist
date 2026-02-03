# test_multilingual.py
"""
Test script for multilingual functionality
"""
from dotenv import load_dotenv
from core.langgraph_workflow import setup_workflow
from core.state import initialize_state

def test_multilingual():
    """Test multilingual responses"""
    load_dotenv()
    
    # Initialize workflow
    workflow = setup_workflow()
    
    # Test cases with different languages
    test_cases = [
        {
            "question": "What are the symptoms of diabetes?",
            "language": "en",
            "expected_language": "en"
        },
        {
            "question": "¿Cuáles son los síntomas de la diabetes?",
            "language": "es",
            "expected_language": "es"
        },
        {
            "question": "What are diabetes symptoms? Please answer in Spanish",
            "language": "en",
            "expected_language": "es"
        },
        {
            "question": "Quels sont les symptômes du diabète?",
            "language": "fr",
            "expected_language": "fr"
        },
        {
            "question": "मधुमेह के लक्षण क्या हैं?",
            "language": "hi",
            "expected_language": "hi"
        }
    ]
    
    print("=== Testing Multilingual Functionality ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['question']}")
        print(f"Expected Language: {test_case['expected_language']}")
        
        # Initialize state
        state = initialize_state()
        state.update({
            "question": test_case["question"],
            "language": test_case["language"],
            "conversation_history": []
        })
        
        # Run workflow
        result = workflow.invoke(state)
        
        print(f"Response Language: {result.get('language', 'unknown')}")
        print(f"Response: {result.get('generation', 'No response')}")
        print("-" * 60)
        
        # Verify language detection
        if result.get('language') == test_case['expected_language']:
            print("✅ Language detection: PASSED")
        else:
            print("❌ Language detection: FAILED")
        print()

if __name__ == "__main__":
    test_multilingual()
