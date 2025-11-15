"""
Quick test to compare TextBlob vs Transformers on your actual data
Run: venv\Scripts\python.exe test_sentiment_comparison.py
"""

import pandas as pd
from textblob import TextBlob

print("="*60)
print("SENTIMENT ANALYSIS COMPARISON TEST")
print("="*60)

# Load data
df = pd.read_csv('raw-data.csv', encoding='utf-8-sig')
df.columns = df.columns.str.strip()

# Get team culture responses (good test case)
culture_df = df[df['Question'].str.contains('team culture', case=False, na=False)]
responses = culture_df['Responses'].head(20).tolist()

print(f"\nTesting on {len(responses)} 'Team Culture' responses")
print("="*60)

# TextBlob analysis
print("\n1. TEXTBLOB ANALYSIS (Current Method)")
print("-"*60)
textblob_results = []
for r in responses:
    try:
        blob = TextBlob(str(r))
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        textblob_results.append((r, sentiment, polarity))
    except:
        textblob_results.append((r, 'Neutral', 0))

for response, sentiment, polarity in textblob_results:
    print(f"{response:25s} → {sentiment:10s} (score: {polarity:5.2f})")

textblob_counts = pd.Series([x[1] for x in textblob_results]).value_counts()
print(f"\nSummary: {dict(textblob_counts)}")

# Check if transformers available
try:
    from transformers import pipeline
    print("\n✅ Transformers library detected!")

    print("\n2. TRANSFORMERS ANALYSIS (Improved Method)")
    print("-"*60)
    print("Loading model (first time takes ~10 seconds)...")

    model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    transformer_results = []
    for r in responses:
        # Preprocess
        processed = str(r).replace('_', ' ')
        if len(processed.split()) <= 2:
            processed = f"This is described as: {processed}"

        result = model(processed, truncation=True, max_length=512)[0]
        transformer_results.append((r, result['label'], result['score']))

    for response, sentiment, confidence in transformer_results:
        print(f"{response:25s} → {sentiment:10s} (confidence: {confidence:.2f})")

    transformer_counts = pd.Series([x[1] for x in transformer_results]).value_counts()
    print(f"\nSummary: {dict(transformer_counts)}")

    # Show differences
    print("\n3. COMPARISON - WHERE THEY DIFFER")
    print("-"*60)
    differences = 0
    for i, (tb, tr) in enumerate(zip(textblob_results, transformer_results)):
        response = tb[0]
        tb_sent = tb[1]
        tr_sent = 'Positive' if tr[1] == 'POSITIVE' else 'Negative'

        if tb_sent != tr_sent:
            differences += 1
            print(f"{response:25s}")
            print(f"  TextBlob:     {tb_sent} (score: {tb[2]:.2f})")
            print(f"  Transformers: {tr_sent} (confidence: {tr[2]:.2f})")
            print()

    print(f"Total differences: {differences}/{len(responses)} ({differences/len(responses)*100:.1f}%)")

    print("\n" + "="*60)
    print("RECOMMENDATION:")
    print("="*60)
    if differences > len(responses) * 0.2:
        print("⚠️  Significant differences found (>20%)")
        print("   → Transformers likely more accurate for your data")
        print("   → Consider upgrading if presenting to leadership")
    else:
        print("✓ Both methods mostly agree")
        print("  → TextBlob may be sufficient for quick analysis")

except ImportError:
    print("\n❌ Transformers library not installed")
    print("\nTo install and see improved results:")
    print("   venv\Scripts\python.exe -m pip install transformers torch")
    print("\nThen run this script again.")

print("\n" + "="*60)
print("Test complete!")
print("="*60)
