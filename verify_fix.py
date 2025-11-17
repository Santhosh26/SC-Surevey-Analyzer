"""
Verify the fix for "More collaboration" issue
"""

from textblob import TextBlob
import pandas as pd
import re

# Copy configurations
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

# Test with FIXED logic
print("\n" + "="*80)
print("VERIFYING FIX: 'More collaboration' with corrected logic")
print("="*80)

response = "More collaboration"
blob = TextBlob(response)
base_polarity = blob.sentiment.polarity

print(f"\nResponse: '{response}'")
print(f"TextBlob base polarity: {base_polarity:.3f}")

sentiment_score = base_polarity
print(f"\nStarting score: {sentiment_score:.3f}")

# Check gap indicator
has_gap_indicator = detect_gap_indicators(response)
print(f"\nGap indicator detected: {has_gap_indicator}")
if has_gap_indicator:
    sentiment_score -= 0.5
    print(f"After gap adjustment (-0.5): {sentiment_score:.3f}")

# Check strength keyword - BUT NOT if gap indicator present
has_strength = contains_keywords(response, STRENGTH_KEYWORDS)
print(f"\nStrength keyword detected: {has_strength}")
if has_strength and not has_gap_indicator:  # FIXED: Only apply if NO gap indicator
    sentiment_score += 0.3
    print(f"After strength adjustment (+0.3): {sentiment_score:.3f}")
else:
    print(f"Strength keyword SKIPPED (gap indicator takes priority)")
    print(f"Score remains: {sentiment_score:.3f}")

# Final classification
print(f"\nFinal sentiment score: {sentiment_score:.3f}")
if sentiment_score > 0.1:
    final_sentiment = 'Positive'
elif sentiment_score < -0.1:
    final_sentiment = 'Negative'
else:
    final_sentiment = 'Neutral'

print(f"Final classification: {final_sentiment}")

if final_sentiment == 'Neutral':
    print("\n[OK] FIX SUCCESSFUL - 'More collaboration' now classified as Neutral!")
else:
    print(f"\n[FAIL] FIX DID NOT WORK - Still classified as {final_sentiment}")

# Test more cases
print("\n" + "="*80)
print("TESTING OTHER CASES")
print("="*80)

test_cases = [
    ("More collaboration", "Neutral"),
    ("Better communication", "Neutral"),
    ("Need more support", "Neutral"),
    ("Trust", "Positive"),  # Should still be positive (no gap)
    ("Innovative", "Positive"),  # Should still be positive (no gap)
]

all_passed = True
for response, expected in test_cases:
    blob = TextBlob(response)
    sentiment_score = blob.sentiment.polarity

    has_gap = detect_gap_indicators(response)
    if has_gap:
        sentiment_score -= 0.5

    has_strength = contains_keywords(response, STRENGTH_KEYWORDS)
    if has_strength and not has_gap:
        sentiment_score += 0.3

    if sentiment_score > 0.1:
        result = 'Positive'
    elif sentiment_score < -0.1:
        result = 'Negative'
    else:
        result = 'Neutral'

    status = "[OK]" if result == expected else f"[FAIL] Expected {expected}"
    print(f"  {status} '{response}' -> {result}")
    if result != expected:
        all_passed = False

print("\n" + "="*80)
if all_passed:
    print("[OK] ALL TESTS PASSED - FIX IS WORKING CORRECTLY!")
else:
    print("[FAIL] SOME TESTS FAILED - REVIEW REQUIRED")
print("="*80)
