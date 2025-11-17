"""
Quick test to verify sentiment analysis integration works correctly
"""

import pandas as pd
from textblob import TextBlob
import re

# Import configurations from app.py
exec(open('app.py').read().split('# ==================== DATA LOADING ====================')[0])

# Test responses from user-reported issues
test_cases = [
    {
        'response': 'More collaboration',
        'question': 'How should our team relationship with PM be different?',
        'expected_new': 'Neutral',  # Should detect gap indicator
        'expected_old': 'Positive'  # TextBlob sees "collaboration" as positive
    },
    {
        'response': 'Listen more',
        'question': "The Buyer's Experience: Our customers are more informed than ever. How does this change how we add value?",
        'expected_new': 'Negative',  # Should detect listening gap
        'expected_old': 'Positive'  # TextBlob sees "listen" as positive
    },
    {
        'response': 'Active listening',
        'question': 'As routine tasks get automated, what becomes the most important, uniquely human ways we add value?',
        'expected_new': 'Negative',  # Should detect listening gap
        'expected_old': 'Neutral'  # TextBlob neutral
    },
    {
        'response': 'POC',
        'question': 'What should we stop doing today?',
        'expected_new': 'Negative',  # Should detect pain point in context
        'expected_old': 'Neutral'  # TextBlob has no sentiment for "POC"
    },
    {
        'response': 'Trust',
        'question': 'As routine tasks get automated, what becomes the most important, uniquely human ways we add value?',
        'expected_new': 'Positive',  # Strength keyword in positive context
        'expected_old': 'Positive'  # TextBlob also positive
    }
]

print("\n" + "=" * 80)
print("SENTIMENT ANALYSIS INTEGRATION TEST")
print("=" * 80)
print("\nTesting user-reported issues...\n")

all_passed = True

for i, test in enumerate(test_cases, 1):
    print(f"Test {i}: \"{test['response']}\"")
    print(f"  Question: {test['question'][:60]}...")

    # Detect question context
    question_context = detect_question_context(test['question'])

    # Run old method (TextBlob)
    blob = TextBlob(test['response'])
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        old_sentiment = 'Positive'
    elif polarity < -0.1:
        old_sentiment = 'Negative'
    else:
        old_sentiment = 'Neutral'

    # Run new method
    new_sentiment, confidence, reasoning = new_contextual_sentiment(
        test['response'], test['question'], question_context
    )

    # Check results
    old_correct = old_sentiment == test['expected_old']
    new_correct = new_sentiment == test['expected_new']

    print(f"  Old Method (TextBlob): {old_sentiment} {'✓' if old_correct else '✗ FAILED'}")
    print(f"  New Method (Q-Aware): {new_sentiment} {'✓' if new_correct else '✗ FAILED'}")
    print(f"  Confidence: {confidence:.2f}")
    print(f"  Reasoning: {reasoning}")

    if not new_correct:
        print(f"  [ERROR] Expected {test['expected_new']}, got {new_sentiment}")
        all_passed = False

    print()

print("=" * 80)
if all_passed:
    print("✓ ALL TESTS PASSED - Sentiment integration working correctly!")
else:
    print("✗ SOME TESTS FAILED - Review results above")
print("=" * 80)
