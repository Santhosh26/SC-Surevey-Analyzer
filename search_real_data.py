import pandas as pd
from validate_latest_fixes import new_contextual_sentiment

df = pd.read_csv('raw-data.csv')

print("="*80)
print("SEARCHING REAL DATA FOR USER-REPORTED ISSUES")
print("="*80)
print()

# Search for START DOING question
print("1. Searching for START DOING question...")
start_q = df[df['Question'].str.contains('START', case=False, na=False)]
print(f"   Found {len(start_q)} responses")

if len(start_q) > 0:
    question_text = start_q.iloc[0]['Question']
    print(f"   Question: {question_text[:70]}...")
    print()

    # Search for problematic responses
    print("2. Testing problematic responses:")
    print("-"*80)

    test_patterns = ['knowledge', 'spoon', 'base']
    for pattern in test_patterns:
        matches = start_q[start_q['Responses'].str.contains(pattern, case=False, na=False)]
        if len(matches) > 0:
            print(f"\n   Responses containing '{pattern}': {len(matches)} found")
            for idx, row in matches.head(3).iterrows():
                response = row['Responses']
                sentiment, confidence, reasoning = new_contextual_sentiment(response, question_text)

                status = "[OK]" if sentiment == 'Positive' else "[ISSUE]"
                print(f"   {status} \"{response}\" -> {sentiment} (confidence: {confidence:.2f})")
                if sentiment != 'Positive':
                    print(f"        Reasoning: {reasoning}")

print()
print("="*80)
print("3. Searching for PM relationship question...")
pm_q = df[df['Question'].str.contains('PM|Product Management|relationship with', case=False, na=False)]
print(f"   Found {len(pm_q)} responses")

if len(pm_q) > 0:
    question_text = pm_q.iloc[0]['Question']
    print(f"   Question: {question_text[:70]}...")
    print()

    # Search for collaboration responses
    collab = pm_q[pm_q['Responses'].str.contains('collab', case=False, na=False)]
    if len(collab) > 0:
        print(f"\n   Responses containing 'collaboration': {len(collab)} found")
        for idx, row in collab.head(5).iterrows():
            response = row['Responses']
            sentiment, confidence, reasoning = new_contextual_sentiment(response, question_text)

            if 'more' in response.lower():
                expected = 'Neutral'
            else:
                expected = 'Positive'

            status = "[OK]" if sentiment == expected else "[ISSUE]"
            print(f"   {status} \"{response}\" -> {sentiment} (expected: {expected}, confidence: {confidence:.2f})")
            if sentiment != expected:
                print(f"        Reasoning: {reasoning}")

print()
print("="*80)
print("SUMMARY")
print("="*80)
print("[SUCCESS] All user-reported issues have been tested with real data")
print("="*80)
