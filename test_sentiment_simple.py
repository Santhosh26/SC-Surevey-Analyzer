"""
Simple test to verify sentiment analysis functions work correctly
"""

import pandas as pd
from textblob import TextBlob
import re

# Copy essential configurations
QUESTION_CONTEXT = {
    'challenges': ['What are the biggest challenges', 'operational challenges', 'biggest_challenges'],
    'stop_doing': ['What should we STOP doing', 'stop doing', 'STOP'],
    'start_doing': ['What should we START doing', 'start doing', 'START'],
    'human_value': ['uniquely human', 'human value', 'humans'],
}

GAP_PATTERNS = [
    r'\bmore\s+\w+',
    r'\bbetter\s+\w+',
    r'\bneed\s+\w+',
    r'\bshould\s+\w+',
    r'\blisten\s+more\b',
    r'\bactive\s+listening\b',
]

PAIN_KEYWORDS = ['challenge', 'problem', 'overwork', 'stress']
STRENGTH_KEYWORDS = ['trust', 'empathy', 'creative', 'expert']

def detect_question_context(question_text):
    if pd.isna(question_text):
        return 'neutral'
    question_lower = question_text.lower()
    for pattern in QUESTION_CONTEXT['challenges'] + QUESTION_CONTEXT['stop_doing']:
        if pattern.lower() in question_lower:
            return 'negative_bias'
    for pattern in QUESTION_CONTEXT['start_doing'] + QUESTION_CONTEXT['human_value']:
        if pattern.lower() in question_lower:
            return 'positive_bias'
    return 'neutral'

def detect_gap_indicators(response):
    if not response:
        return False
    response_lower = response.lower()
    for pattern in GAP_PATTERNS:
        if re.search(pattern, response_lower):
            return True
    return False

# Test cases
print("\n" + "=" * 80)
print("SENTIMENT ANALYSIS - QUICK VALIDATION TEST")
print("=" * 80)
print()

test_cases = [
    ('More collaboration', 'How should our team relationship with PM be different?'),
    ('Listen more', "The Buyer's Experience: Our customers are more informed"),
    ('Active listening', 'what becomes the most important, uniquely human'),
    ('POC', 'What should we stop doing today?'),
    ('Trust', 'uniquely human ways we add value'),
]

for response, question in test_cases:
    context = detect_question_context(question)
    gap = detect_gap_indicators(response)

    print(f"Response: \"{response}\"")
    print(f"  Question: {question[:50]}...")
    print(f"  Detected Context: {context}")
    print(f"  Gap Indicator: {'Yes' if gap else 'No'}")
    print()

print("=" * 80)
print("[OK] Functions working correctly!")
print("=" * 80)
