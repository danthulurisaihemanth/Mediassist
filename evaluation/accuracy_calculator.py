# evaluation/accuracy_calculator.py
"""
Accuracy calculation module for evaluating chatbot responses
"""

import re
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class AccuracyCalculator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    
    def calculate_keyword_match(self, response: str, expected_keywords: List[str]) -> float:
        """
        Calculate keyword match score (0-1)
        Checks if expected keywords appear in the response
        """
        if not response or not expected_keywords:
            return 0.0
        
        response_lower = response.lower()
        matched_keywords = []
        
        for keyword in expected_keywords:
            keyword_lower = keyword.lower()
            # Check if keyword or its variations appear in response
            if keyword_lower in response_lower:
                matched_keywords.append(keyword)
            else:
                # Check for word boundaries and partial matches
                pattern = r'\b' + re.escape(keyword_lower) + r'\w*'
                if re.search(pattern, response_lower):
                    matched_keywords.append(keyword)
        
        return len(matched_keywords) / len(expected_keywords) if expected_keywords else 0.0
    
    def calculate_semantic_similarity(self, response: str, expected_keywords: List[str]) -> float:
        """
        Calculate semantic similarity using TF-IDF and cosine similarity
        """
        if not response:
            return 0.0
        
        try:
            # Create documents: response and expected keywords as a document
            expected_doc = " ".join(expected_keywords)
            documents = [response, expected_doc]
            
            # Vectorize
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception:
            return 0.0
    
    def calculate_response_quality(self, response: str) -> Dict[str, float]:
        """
        Calculate response quality metrics
        """
        if not response:
            return {
                "length_score": 0.0,
                "completeness_score": 0.0,
                "medical_terminology_score": 0.0
            }
        
        # Length score (optimal length: 50-200 words)
        word_count = len(response.split())
        if 50 <= word_count <= 200:
            length_score = 1.0
        elif word_count < 50:
            length_score = word_count / 50.0
        else:
            length_score = max(0.0, 1.0 - (word_count - 200) / 200.0)
        
        # Completeness score (check for medical indicators)
        medical_indicators = ["symptom", "treatment", "cause", "prevent", "diagnosis", 
                             "medical", "health", "doctor", "patient", "condition"]
        indicator_count = sum(1 for indicator in medical_indicators if indicator.lower() in response.lower())
        completeness_score = min(1.0, indicator_count / 3.0)
        
        # Medical terminology score
        medical_terms = ["medication", "therapy", "diagnosis", "symptom", "treatment",
                         "condition", "disease", "disorder", "syndrome", "pathology"]
        term_count = sum(1 for term in medical_terms if term.lower() in response.lower())
        medical_terminology_score = min(1.0, term_count / 2.0)
        
        return {
            "length_score": length_score,
            "completeness_score": completeness_score,
            "medical_terminology_score": medical_terminology_score
        }
    
    def calculate_source_accuracy(self, actual_source: str, expected_source: str) -> float:
        """Check if the response came from the expected source"""
        if actual_source == expected_source:
            return 1.0
        # Partial credit for related sources
        if expected_source == "medical_knowledge" and actual_source in ["retrieved_docs", "llm_knowledge"]:
            return 0.8
        return 0.5
    
    def calculate_overall_accuracy(self, response: str, test_case: Dict) -> Dict[str, float]:
        """
        Calculate overall accuracy score for a single test case
        Returns a dictionary with all metrics
        """
        keyword_match = self.calculate_keyword_match(response, test_case["expected_keywords"])
        semantic_sim = self.calculate_semantic_similarity(response, test_case["expected_keywords"])
        quality_metrics = self.calculate_response_quality(response)
        
        # Weighted accuracy calculation
        accuracy_scores = {
            "keyword_match": keyword_match,
            "semantic_similarity": semantic_sim,
            "length_score": quality_metrics["length_score"],
            "completeness_score": quality_metrics["completeness_score"],
            "medical_terminology_score": quality_metrics["medical_terminology_score"]
        }
        
        # Overall accuracy (weighted average)
        weights = {
            "keyword_match": 0.3,
            "semantic_similarity": 0.3,
            "length_score": 0.1,
            "completeness_score": 0.15,
            "medical_terminology_score": 0.15
        }
        
        overall_accuracy = sum(
            accuracy_scores[metric] * weights[metric]
            for metric in weights.keys()
        )
        
        accuracy_scores["overall_accuracy"] = overall_accuracy
        
        return accuracy_scores
    
    def evaluate_batch(self, responses: List[Tuple[str, Dict]]) -> Dict[str, any]:
        """
        Evaluate a batch of responses
        responses: List of tuples (response_text, test_case_dict)
        """
        results = []
        total_accuracy = 0.0
        
        for response, test_case in responses:
            accuracy_scores = self.calculate_overall_accuracy(response, test_case)
            accuracy_scores["question"] = test_case["question"]
            accuracy_scores["difficulty"] = test_case["difficulty"]
            accuracy_scores["category"] = test_case["expected_category"]
            results.append(accuracy_scores)
            total_accuracy += accuracy_scores["overall_accuracy"]
        
        avg_accuracy = total_accuracy / len(responses) if responses else 0.0
        
        # Calculate accuracy by difficulty
        accuracy_by_difficulty = {}
        accuracy_by_category = {}
        
        for result in results:
            diff = result["difficulty"]
            cat = result["category"]
            
            if diff not in accuracy_by_difficulty:
                accuracy_by_difficulty[diff] = {"total": 0, "sum": 0.0}
            accuracy_by_difficulty[diff]["total"] += 1
            accuracy_by_difficulty[diff]["sum"] += result["overall_accuracy"]
            
            if cat not in accuracy_by_category:
                accuracy_by_category[cat] = {"total": 0, "sum": 0.0}
            accuracy_by_category[cat]["total"] += 1
            accuracy_by_category[cat]["sum"] += result["overall_accuracy"]
        
        # Calculate averages
        for diff in accuracy_by_difficulty:
            accuracy_by_difficulty[diff] = accuracy_by_difficulty[diff]["sum"] / accuracy_by_difficulty[diff]["total"]
        
        for cat in accuracy_by_category:
            accuracy_by_category[cat] = accuracy_by_category[cat]["sum"] / accuracy_by_category[cat]["total"]
        
        return {
            "average_accuracy": avg_accuracy,
            "total_tests": len(responses),
            "accuracy_by_difficulty": accuracy_by_difficulty,
            "accuracy_by_category": accuracy_by_category,
            "detailed_results": results
        }
