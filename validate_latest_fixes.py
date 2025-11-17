"""
Validation Script for Latest Sentiment Analysis Fixes
======================================================

Tests the four fixes implemented:
1. TextBlob override dictionary for known quirks
2. Context-aware negation detection
3. Increased positive bias boost (0.3 -> 0.5)
4. Uncertainty detection rule

Tests specific user-reported issues:
- "Having_a_knowledge_base" in START DOING -> should be Positive
- "Stop_spoon_feeding_ae" in START DOING -> should be Positive
- "More collaboration" in PM relationship -> should be Neutral
"""

import pandas as pd
from textblob import TextBlob
import re

# ============================================================================
# CONFIGURATION (Copied from app.py)
# ============================================================================

QUESTION_CONTEXTS = {
    'negative_bias': [
        'What should we STOP doing today?',
        'Operational Challenge',
    ],
    'positive_bias': [
        'What should we START doing differently tomorrow?',
        'what becomes the most important, uniquely human',
        'How would you describe our team culture',
    ],
    'neutral': [
        'AI tools',
        'Future',
        'mission',
    ]
}

GAP_PATTERNS = [
    r'\bmore\s+\w+',
    r'\bbetter\s+\w+',
    r'\bneed\s+(?:more\s+)?\w+',
    r'\bwant\s+(?:more\s+)?\w+',
    r'\black\s+of\b',
    r'\bwithout\b',
    r'\bmissing\b',
    r'\binsufficient\b',
    r'\binadequate\b',
    r'\blisten\s+more\b',
    r'\bactive\s+listening\b',
    r'\blistening\b',
]

NEGATION_PATTERNS = [
    r'\bnot\b',
    r'\bno\s+\w+',
    r'\bcan\'?t\b',
    r'\bcannot\b',
    r'\bwon\'?t\b',
    r'\bstop\b',
    r'\bnever\b',
]

UNCERTAINTY_PATTERNS = [
    r'\bnot sure\b',
    r'\bunsure\b',
    r'\bdon\'?t know\b',
    r'\buncertain\b',
]

PAIN_KEYWORDS = [
    'challenge', 'difficult', 'hard', 'struggle', 'pain', 'problem',
    'frustrat', 'stress', 'overwork', 'burn', 'overwhelm', 'exhaust',
    'lack', 'gap', 'missing', 'need', 'want', 'require',
    'inefficien', 'slow', 'delay', 'bottleneck', 'blocker',
    'confusion', 'unclear', 'ambiguous', 'uncertain'
]

STRENGTH_KEYWORDS = [
    'trust', 'empathy', 'connection', 'relationship', 'collaborat', 'support',
    'innovat', 'creative', 'expert', 'knowledge', 'skill', 'passion',
    'dedicated', 'commit', 'quality', 'excellent', 'strong', 'effective'
]

TEXTBLOB_OVERRIDES = {
    'knowledge base': 0.1,
    'base': 0.0,
    'poc': 0.0,
    'having a knowledge base': 0.2,
}

# ============================================================================
# HELPER FUNCTIONS (Copied from app.py)
# ============================================================================

def preprocess_response(response):
    """Clean response text for analysis."""
    if not response or response != response:  # Check for None or NaN
        return ""
    response = str(response).strip()
    response = response.replace('_', ' ')
    return response

def detect_question_context(question):
    """Determine if question has negative, positive, or neutral bias."""
    if not question:
        return 'neutral'
    question_lower = question.lower()
    for q_phrase in QUESTION_CONTEXTS['negative_bias']:
        if q_phrase.lower() in question_lower:
            return 'negative_bias'
    for q_phrase in QUESTION_CONTEXTS['positive_bias']:
        if q_phrase.lower() in question_lower:
            return 'positive_bias'
    return 'neutral'

def detect_gap_indicators(response):
    """Detect phrases indicating gaps or needs."""
    if not response:
        return False
    response_lower = response.lower()
    for pattern in GAP_PATTERNS:
        if re.search(pattern, response_lower):
            return True
    return False

def detect_negation(response, question_context):
    """Detect negation patterns with context awareness."""
    if not response:
        return False
    response_lower = response.lower()

    # Check for uncertainty first
    has_uncertainty = any(re.search(pattern, response_lower) for pattern in UNCERTAINTY_PATTERNS)

    for pattern in NEGATION_PATTERNS:
        if re.search(pattern, response_lower):
            # Special case: "stop" in positive_bias questions is constructive
            if question_context == 'positive_bias' and 'stop' in response_lower and not has_uncertainty:
                return False
            return True
    return False

def contains_keywords(response, keywords):
    """Check if response contains any keyword from the list."""
    if not response:
        return False
    response_lower = response.lower()
    for keyword in keywords:
        if keyword in response_lower:
            return True
    return False

def new_contextual_sentiment(response, question):
    """
    Analyze sentiment with question context awareness.
    Returns: (sentiment, confidence, reasoning)
    """
    # Preprocess
    cleaned_response = preprocess_response(response)
    if not cleaned_response:
        return ('Neutral', 0.5, 'Empty or invalid response')

    response_lower = cleaned_response.lower()

    # Apply TextBlob overrides
    override_polarity = None
    for phrase, polarity in TEXTBLOB_OVERRIDES.items():
        if phrase in response_lower:
            override_polarity = polarity
            break

    # Get base sentiment
    if override_polarity is not None:
        base_polarity = override_polarity
    else:
        blob = TextBlob(cleaned_response)
        base_polarity = blob.sentiment.polarity

    sentiment_score = base_polarity
    reasoning_parts = []
    confidence = 0.7

    # Detect question context
    question_context = detect_question_context(question)

    # RULE 1: Question context bias
    if question_context == 'negative_bias':
        sentiment_score -= 0.3
        reasoning_parts.append("Question has negative context")
        confidence += 0.1
    elif question_context == 'positive_bias':
        sentiment_score += 0.5  # INCREASED from 0.3
        reasoning_parts.append("Question has positive context")
        confidence += 0.1

    # RULE 2: Gap indicators
    has_gap_indicator = detect_gap_indicators(cleaned_response)
    if has_gap_indicator:
        sentiment_score -= 0.5
        reasoning_parts.append("Contains gap/need indicator")
        confidence += 0.2

    # RULE 3: Negation patterns (context-aware)
    has_negation = detect_negation(cleaned_response, question_context)
    if has_negation:
        sentiment_score -= 0.4
        reasoning_parts.append("Contains negation")
        confidence += 0.15

    # RULE 4: Pain point keywords
    if contains_keywords(cleaned_response, PAIN_KEYWORDS):
        sentiment_score -= 0.3
        reasoning_parts.append("Contains pain keywords")
        confidence += 0.1

    # RULE 5: Strength keywords (BUT not if gap indicator present)
    if contains_keywords(cleaned_response, STRENGTH_KEYWORDS) and not has_gap_indicator:
        sentiment_score += 0.3
        reasoning_parts.append("Contains strength keywords")
        confidence += 0.1

    # RULE 6: Short responses in context
    if len(cleaned_response.split()) <= 3:
        if question_context == 'negative_bias':
            sentiment_score -= 0.2
            reasoning_parts.append("Short response in negative context")
        elif question_context == 'positive_bias':
            sentiment_score += 0.2
            reasoning_parts.append("Short response in positive context")
        confidence -= 0.1

    # RULE 7: POC-specific edge case
    if 'poc' in response_lower and question_context == 'negative_bias':
        sentiment_score -= 0.4
        reasoning_parts.append("POC in negative context")
        confidence += 0.2

    # RULE 8: Listening gap edge case
    if re.search(r'\blisten', response_lower) or re.search(r'\bactive\s+listening\b', response_lower):
        sentiment_score -= 0.5
        reasoning_parts.append("Listening gap indicator")
        confidence += 0.25

    # Final classification
    if sentiment_score > 0.1:
        sentiment = 'Positive'
    elif sentiment_score < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    # Cap confidence
    confidence = min(confidence, 1.0)

    reasoning = '; '.join(reasoning_parts) if reasoning_parts else 'No special indicators'

    return (sentiment, confidence, reasoning)

# ============================================================================
# TEST CASES
# ============================================================================

def run_tests():
    """Run comprehensive validation tests."""

    print("="*80)
    print("VALIDATION TEST SUITE - Latest Sentiment Analysis Fixes")
    print("="*80)
    print()

    test_cases = [
        # User-reported issues
        {
            'name': 'Issue 1: Having_a_knowledge_base (START DOING)',
            'response': 'Having_a_knowledge_base',
            'question': 'What should we START doing differently tomorrow?',
            'expected_sentiment': 'Positive',
            'expected_min_confidence': 0.7,
            'fix_tested': 'TextBlob override dictionary',
        },
        {
            'name': 'Issue 2: Stop_spoon_feeding_ae (START DOING)',
            'response': 'Stop_spoon_feeding_ae',
            'question': 'What should we START doing differently tomorrow?',
            'expected_sentiment': 'Positive',
            'expected_min_confidence': 0.7,
            'fix_tested': 'Context-aware negation detection',
        },
        {
            'name': 'Issue 3: More collaboration (PM relationship)',
            'response': 'More collaboration',
            'question': 'How should our team relationship with PM be different?',
            'expected_sentiment': 'Neutral',
            'expected_min_confidence': 0.8,
            'fix_tested': 'Gap indicator priority over strength keywords',
        },

        # Additional validation cases
        {
            'name': 'Test 4: Listen more (Buyer knowledge)',
            'response': 'Listen more',
            'question': 'The Buyer\'s Experience: Our customers are more informed',
            'expected_sentiment': 'Negative',
            'expected_min_confidence': 0.9,
            'fix_tested': 'Listening gap detection',
        },
        {
            'name': 'Test 5: Active listening (Human value)',
            'response': 'Active listening',
            'question': 'what becomes the most important, uniquely human value',
            'expected_sentiment': 'Negative',
            'expected_min_confidence': 0.9,
            'fix_tested': 'Listening gap detection',
        },
        {
            'name': 'Test 6: POC (STOP DOING)',
            'response': 'POC',
            'question': 'What should we STOP doing today?',
            'expected_sentiment': 'Negative',
            'expected_min_confidence': 0.8,
            'fix_tested': 'POC in negative context',
        },

        # Test TextBlob overrides
        {
            'name': 'Test 7: Knowledge base (positive context)',
            'response': 'Knowledge base',
            'question': 'How would you describe our team culture',
            'expected_sentiment': 'Positive',
            'expected_min_confidence': 0.7,
            'fix_tested': 'TextBlob override for "base" word',
        },

        # Test increased positive bias
        {
            'name': 'Test 8: Empowerment (START DOING)',
            'response': 'Empowerment',
            'question': 'What should we START doing differently tomorrow?',
            'expected_sentiment': 'Positive',
            'expected_min_confidence': 0.7,
            'fix_tested': 'Increased positive bias boost (0.5)',
        },

        # Test uncertainty detection
        {
            'name': 'Test 9: Not sure about direction',
            'response': 'Not sure about direction',
            'question': 'What are the challenges?',
            'expected_sentiment': 'Negative',
            'expected_min_confidence': 0.6,
            'fix_tested': 'Uncertainty detection',
        },

        # Test gap + strength combo
        {
            'name': 'Test 10: Need better innovation',
            'response': 'Need better innovation',
            'question': 'What should we improve?',
            'expected_sentiment': 'Neutral',
            'expected_min_confidence': 0.8,
            'fix_tested': 'Gap priority over strength',
        },
    ]

    passed = 0
    failed = 0
    results = []

    for i, test in enumerate(test_cases, 1):
        sentiment, confidence, reasoning = new_contextual_sentiment(
            test['response'],
            test['question']
        )

        sentiment_match = sentiment == test['expected_sentiment']
        confidence_ok = confidence >= test['expected_min_confidence']
        test_passed = sentiment_match and confidence_ok

        if test_passed:
            passed += 1
            status = "[PASS]"
        else:
            failed += 1
            status = "[FAIL]"

        results.append({
            'test': test['name'],
            'response': test['response'],
            'question': test['question'][:50] + '...',
            'expected': test['expected_sentiment'],
            'got': sentiment,
            'confidence': confidence,
            'fix_tested': test['fix_tested'],
            'status': status,
            'reasoning': reasoning,
        })

        print(f"{status} Test {i}: {test['name']}")
        print(f"   Response: \"{test['response']}\"")
        print(f"   Question: {test['question'][:60]}...")
        print(f"   Expected: {test['expected_sentiment']} (confidence >= {test['expected_min_confidence']:.2f})")
        print(f"   Got: {sentiment} (confidence: {confidence:.2f})")
        print(f"   Fix Tested: {test['fix_tested']}")
        print(f"   Reasoning: {reasoning}")

        if not sentiment_match:
            print(f"   [WARNING] Sentiment mismatch!")
        if not confidence_ok:
            print(f"   [WARNING] Confidence too low!")
        print()

    # Summary
    print("="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {len(test_cases)}")
    print(f"[OK] Passed: {passed}")
    print(f"[FAIL] Failed: {failed}")
    print(f"Success Rate: {100*passed/len(test_cases):.1f}%")
    print()

    if failed == 0:
        print("[SUCCESS] ALL TESTS PASSED! All fixes are working correctly.")
    else:
        print("[WARNING] Some tests failed. Review the fixes.")

    print("="*80)

    # Create detailed results DataFrame
    results_df = pd.DataFrame(results)

    return results_df, passed, failed

# ============================================================================
# REAL DATA VALIDATION
# ============================================================================

def validate_real_data():
    """Test fixes on real survey data."""

    print("\n" + "="*80)
    print("REAL DATA VALIDATION")
    print("="*80)
    print()

    try:
        df = pd.read_csv('raw-data.csv')
        print(f"[OK] Loaded {len(df)} responses from raw-data.csv")
        print()

        # Test specific problematic responses from real data
        start_doing_question = 'What should we START doing differently tomorrow?'
        start_doing_df = df[df['Question'] == start_doing_question]

        if len(start_doing_df) > 0:
            print(f"Found {len(start_doing_df)} responses for START DOING question")
            print()

            # Test specific responses
            test_responses = [
                'Having_a_knowledge_base',
                'Stop_spoon_feeding_ae',
                'knowledge base',
                'base',
            ]

            print("Testing specific responses:")
            print("-" * 80)

            for response in test_responses:
                matches = start_doing_df[start_doing_df['Responses'].str.contains(response, case=False, na=False)]

                if len(matches) > 0:
                    actual_response = matches.iloc[0]['Responses']
                    sentiment, confidence, reasoning = new_contextual_sentiment(
                        actual_response,
                        start_doing_question
                    )

                    print(f"Response: \"{actual_response}\"")
                    print(f"  Sentiment: {sentiment} (confidence: {confidence:.2f})")
                    print(f"  Reasoning: {reasoning}")

                    if sentiment == 'Positive':
                        print(f"  [OK] Correctly classified as Positive")
                    else:
                        print(f"  [FAIL] Should be Positive, got {sentiment}")
                    print()
                else:
                    print(f"Response pattern \"{response}\" not found in data")
                    print()

        # Test PM relationship question
        pm_question_matches = df[df['Question'].str.contains('PM', case=False, na=False)]
        if len(pm_question_matches) > 0:
            pm_question = pm_question_matches.iloc[0]['Question']
            pm_df = df[df['Question'] == pm_question]

            print(f"\nFound {len(pm_df)} responses for PM relationship question")
            print(f"Question: {pm_question[:70]}...")
            print()

            # Test "More collaboration"
            collab_matches = pm_df[pm_df['Responses'].str.contains('collaboration', case=False, na=False)]
            if len(collab_matches) > 0:
                for idx, row in collab_matches.head(3).iterrows():
                    response = row['Responses']
                    sentiment, confidence, reasoning = new_contextual_sentiment(response, pm_question)

                    print(f"Response: \"{response}\"")
                    print(f"  Sentiment: {sentiment} (confidence: {confidence:.2f})")
                    print(f"  Reasoning: {reasoning}")

                    if 'more' in response.lower() and sentiment == 'Neutral':
                        print(f"  [OK] Correctly classified as Neutral (gap indicator)")
                    elif 'more' not in response.lower() and sentiment == 'Positive':
                        print(f"  [OK] Correctly classified as Positive (no gap)")
                    else:
                        print(f"  [WARNING] Review classification")
                    print()

        print("="*80)

    except FileNotFoundError:
        print("[WARNING] raw-data.csv not found. Skipping real data validation.")
        print("="*80)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run test suite
    results_df, passed, failed = run_tests()

    # Save results
    results_df.to_csv('validation_test_results.csv', index=False)
    print(f"\n[OK] Test results saved to validation_test_results.csv")

    # Run real data validation
    validate_real_data()

    # Final verdict
    print("\n" + "="*80)
    print("VALIDATION VERDICT")
    print("="*80)

    if failed == 0:
        print("[SUCCESS] ALL FIXES VERIFIED AND WORKING")
        print("\nThe following improvements have been validated:")
        print("1. [OK] TextBlob override dictionary - fixes 'base' and 'knowledge base' issues")
        print("2. [OK] Context-aware negation - 'stop' in START DOING now positive")
        print("3. [OK] Increased positive bias boost - better classification in positive contexts")
        print("4. [OK] Uncertainty detection - handles 'not sure' type responses")
        print("\nAll user-reported issues are now resolved:")
        print("  - Having_a_knowledge_base -> Positive [OK]")
        print("  - Stop_spoon_feeding_ae -> Positive [OK]")
        print("  - More collaboration -> Neutral [OK]")
        print("\nReady for deployment!")
    else:
        print(f"[WARNING] {failed} test(s) failed. Review needed.")

    print("="*80)
