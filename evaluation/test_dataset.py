# evaluation/test_dataset.py
"""
Medical Question Test Dataset for Accuracy Evaluation
Each test case includes: question, expected_keywords, expected_category, difficulty
"""

TEST_DATASET = [
    {
        "question": "What are the symptoms of diabetes?",
        "expected_keywords": ["thirst", "urination", "fatigue", "weight", "blood sugar"],
        "expected_category": "symptoms",
        "difficulty": "easy",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to treat a headache?",
        "expected_keywords": ["rest", "hydration", "pain", "medication", "stress"],
        "expected_category": "treatment",
        "difficulty": "easy",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What causes high blood pressure?",
        "expected_keywords": ["diet", "exercise", "stress", "genetics", "age", "salt"],
        "expected_category": "causes",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What are the symptoms of COVID-19?",
        "expected_keywords": ["fever", "cough", "breathing", "fatigue", "loss", "taste", "smell"],
        "expected_category": "symptoms",
        "difficulty": "easy",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to prevent heart disease?",
        "expected_keywords": ["exercise", "diet", "smoking", "cholesterol", "blood pressure"],
        "expected_category": "prevention",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What is the treatment for migraine?",
        "expected_keywords": ["medication", "rest", "dark", "quiet", "hydration", "triggers"],
        "expected_category": "treatment",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What are the side effects of antibiotics?",
        "expected_keywords": ["nausea", "diarrhea", "allergic", "resistance", "stomach"],
        "expected_category": "side_effects",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to lower cholesterol naturally?",
        "expected_keywords": ["diet", "exercise", "fiber", "omega", "reduce", "saturated"],
        "expected_category": "treatment",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What causes asthma?",
        "expected_keywords": ["genetics", "environment", "allergens", "irritants", "triggers"],
        "expected_category": "causes",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What are the symptoms of depression?",
        "expected_keywords": ["sadness", "loss", "interest", "sleep", "appetite", "energy", "concentration"],
        "expected_category": "symptoms",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to treat insomnia?",
        "expected_keywords": ["sleep", "hygiene", "routine", "relaxation", "medication", "therapy"],
        "expected_category": "treatment",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What is the best diet for diabetes?",
        "expected_keywords": ["carbohydrates", "fiber", "protein", "vegetables", "sugar", "blood"],
        "expected_category": "diet",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What causes acid reflux?",
        "expected_keywords": ["stomach", "acid", "diet", "lifestyle", "obesity", "smoking"],
        "expected_category": "causes",
        "difficulty": "easy",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to manage anxiety?",
        "expected_keywords": ["therapy", "meditation", "breathing", "exercise", "lifestyle", "support"],
        "expected_category": "treatment",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What are the symptoms of pneumonia?",
        "expected_keywords": ["cough", "fever", "chest", "pain", "breathing", "fatigue"],
        "expected_category": "symptoms",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to prevent flu?",
        "expected_keywords": ["vaccine", "hygiene", "washing", "hands", "avoid", "contact"],
        "expected_category": "prevention",
        "difficulty": "easy",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What causes kidney stones?",
        "expected_keywords": ["dehydration", "diet", "calcium", "oxalate", "genetics", "urine"],
        "expected_category": "causes",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What are the symptoms of hypothyroidism?",
        "expected_keywords": ["fatigue", "weight", "gain", "cold", "depression", "hair", "loss"],
        "expected_category": "symptoms",
        "difficulty": "hard",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to treat seasonal allergies?",
        "expected_keywords": ["antihistamines", "avoid", "allergens", "nasal", "spray", "medication"],
        "expected_category": "treatment",
        "difficulty": "easy",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What is the normal blood pressure range?",
        "expected_keywords": ["120", "80", "systolic", "diastolic", "mmhg", "normal"],
        "expected_category": "information",
        "difficulty": "easy",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What causes osteoporosis?",
        "expected_keywords": ["age", "calcium", "vitamin", "d", "hormones", "bone", "density"],
        "expected_category": "causes",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to manage chronic pain?",
        "expected_keywords": ["medication", "therapy", "exercise", "lifestyle", "support", "treatment"],
        "expected_category": "treatment",
        "difficulty": "hard",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What are the symptoms of anemia?",
        "expected_keywords": ["fatigue", "weakness", "pale", "shortness", "breath", "dizziness"],
        "expected_category": "symptoms",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "How to prevent stroke?",
        "expected_keywords": ["blood pressure", "diet", "exercise", "smoking", "cholesterol", "lifestyle"],
        "expected_category": "prevention",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    },
    {
        "question": "What causes arthritis?",
        "expected_keywords": ["age", "injury", "genetics", "infection", "autoimmune", "wear"],
        "expected_category": "causes",
        "difficulty": "medium",
        "expected_source": "medical_knowledge"
    }
]

def get_test_dataset():
    """Return the test dataset"""
    return TEST_DATASET

def get_dataset_by_difficulty(difficulty):
    """Filter dataset by difficulty level"""
    return [test for test in TEST_DATASET if test["difficulty"] == difficulty]

def get_dataset_stats():
    """Get statistics about the test dataset"""
    total = len(TEST_DATASET)
    by_difficulty = {}
    by_category = {}
    
    for test in TEST_DATASET:
        diff = test["difficulty"]
        cat = test["expected_category"]
        by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
        by_category[cat] = by_category.get(cat, 0) + 1
    
    return {
        "total": total,
        "by_difficulty": by_difficulty,
        "by_category": by_category
    }
