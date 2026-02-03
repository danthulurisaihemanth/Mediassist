# evaluation/run_evaluation.py
"""
Main evaluation script to test chatbot accuracy
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.langgraph_workflow import setup_workflow
from core.state import initialize_state
from evaluation.test_dataset import get_test_dataset
from evaluation.accuracy_calculator import AccuracyCalculator

def run_evaluation():
    """Run comprehensive evaluation of the chatbot"""
    print("=" * 60)
    print("MediGenius Chatbot Accuracy Evaluation")
    print("=" * 60)
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Initialize workflow and calculator
    print("Initializing workflow...")
    workflow = setup_workflow()
    calculator = AccuracyCalculator()
    
    # Get test dataset
    test_dataset = get_test_dataset()
    print(f"Loaded {len(test_dataset)} test cases")
    print()
    
    # Run evaluation
    print("Running evaluation...")
    print("-" * 60)
    
    responses = []
    for i, test_case in enumerate(test_dataset, 1):
        print(f"[{i}/{len(test_dataset)}] Testing: {test_case['question']}")
        
        # Initialize state
        state = initialize_state()
        state.update({
            "question": test_case["question"],
            "language": "en",
            "conversation_history": []
        })
        
        # Get response
        try:
            result = workflow.invoke(state)
            response = result.get('generation', '')
            responses.append((response, test_case))
            print(f"  ✓ Response received ({len(response)} chars)")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            responses.append(("", test_case))
        
        print()
    
    # Calculate accuracy
    print("Calculating accuracy metrics...")
    print("-" * 60)
    
    evaluation_results = calculator.evaluate_batch(responses)
    
    # Display results
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"\nAverage Accuracy: {evaluation_results['average_accuracy']:.2%}")
    print(f"Total Tests: {evaluation_results['total_tests']}")
    
    print("\nAccuracy by Difficulty:")
    for difficulty, accuracy in evaluation_results['accuracy_by_difficulty'].items():
        print(f"  {difficulty.capitalize()}: {accuracy:.2%}")
    
    print("\nAccuracy by Category:")
    for category, accuracy in evaluation_results['accuracy_by_category'].items():
        print(f"  {category.capitalize()}: {accuracy:.2%}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"evaluation_results_{timestamp}.json"
    
    # Prepare results for JSON
    json_results = {
        "timestamp": timestamp,
        "average_accuracy": evaluation_results['average_accuracy'],
        "total_tests": evaluation_results['total_tests'],
        "accuracy_by_difficulty": evaluation_results['accuracy_by_difficulty'],
        "accuracy_by_category": evaluation_results['accuracy_by_category'],
        "detailed_results": [
            {
                "question": r["question"],
                "difficulty": r["difficulty"],
                "category": r["category"],
                "overall_accuracy": r["overall_accuracy"],
                "keyword_match": r["keyword_match"],
                "semantic_similarity": r["semantic_similarity"]
            }
            for r in evaluation_results['detailed_results']
        ]
    }
    
    with open(results_file, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    
    # Check if accuracy meets threshold
    threshold = 0.80
    if evaluation_results['average_accuracy'] >= threshold:
        print(f"\n✅ SUCCESS: Accuracy ({evaluation_results['average_accuracy']:.2%}) meets threshold ({threshold:.0%})")
    else:
        print(f"\n❌ WARNING: Accuracy ({evaluation_results['average_accuracy']:.2%}) below threshold ({threshold:.0%})")
    
    return evaluation_results

if __name__ == "__main__":
    results = run_evaluation()
