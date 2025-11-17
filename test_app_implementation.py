"""
Test the actual app.py implementation for "More collaboration" issue
"""

import sys
import importlib.util

# Load app.py as a module
spec = importlib.util.spec_from_file_location("app", "app.py")
app = importlib.util.module_from_spec(spec)

# Manually define the required functions since we can't execute the full Streamlit app
# We'll just test the sentiment logic

from textblob import TextBlob
import pandas as pd
import re

# Copy configurations from app.py
STRENGTH_KEYWORDS = [
    'trust', 'empathy', 'connection', 'relationship', 'collaborat', 'support',
    'innovat', 'creative', 'expert', 'knowledge', 'skill', 'passion',
    'dedicated', 'commit', 'quality', 'excellent', 'strong', 'effective'
]

GAP_PATTERNS = [
    r'\bmore\s+\w+',
    r'\bbetter\s+\w+',
    r'\bneed\s+\w+',
]

def detect_gap_indicators(response):
    if not response:
        return False
    response_lower = response.lower()
    for pattern in GAP_PATTERNS:
        if re.search(pattern, response_lower):
            return True
    return False

def contains_keywords(response, keywords):
    if not response:
        return False
    response_lower = response.lower()
    for keyword in keywords:
        if keyword in response_lower:
            return True
    return False

# Test "More collaboration"
print("\n" + "="*80)
print("TESTING 'More collaboration' with actual logic from app.py")
print("="*80)

response = "More collaboration"
blob = TextBlob(response)
base_polarity = blob.sentiment.polarity

print(f"\nResponse: '{response}'")
print(f"TextBlob base polarity: {base_polarity:.3f}")

sentiment_score = base_polarity
print(f"\nStarting score: {sentiment_score:.3f}")

# Check gap indicator
has_gap = detect_gap_indicators(response)
print(f"\nGap indicator detected: {has_gap}")
if has_gap:
    sentiment_score -= 0.5
    print(f"After gap adjustment (-0.5): {sentiment_score:.3f}")

# Check strength keyword
has_strength = contains_keywords(response, STRENGTH_KEYWORDS)
print(f"\nStrength keyword detected: {has_strength}")
if has_strength:
    sentiment_score += 0.3
    print(f"After strength adjustment (+0.3): {sentiment_score:.3f}")

# Final classification
print(f"\nFinal sentiment score: {sentiment_score:.3f}")
if sentiment_score > 0.1:
    final_sentiment = 'Positive'
elif sentiment_score < -0.1:
    final_sentiment = 'Negative'
else:
    final_sentiment = 'Neutral'

print(f"Final classification: {final_sentiment}")

print("\n" + "="*80)
print("PROBLEM IDENTIFIED:")
print("="*80)
print("The gap indicator (-0.5) is being offset by strength keyword (+0.3)")
print("resulting in Positive classification instead of Neutral.")
print("\nSOLUTION: Gap indicators should override strength keywords.")
print("="*80)
