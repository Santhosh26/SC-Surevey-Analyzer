"""
Sentiment Analysis Validator - Testing Script
==============================================

This script validates and compares sentiment analysis approaches for survey responses.

Problem:
    Current TextBlob approach classifies grammatical sentiment (word polarity)
    instead of contextual sentiment (what the response means in survey context).

    Examples:
    - "More collaboration" → Positive (WRONG - indicates a gap)
    - "Listen more" → Positive (WRONG - indicates missing behavior)
    - "POC" in Q13 Stop Doing → Neutral (WRONG - it's a pain point)

Solution:
    Question-aware rule-based sentiment analysis that understands:
    - Question context (Q12/Q13 = pain points, Q14 = initiatives)
    - Gap indicators ("more X", "need X", "better X")
    - Negation patterns ("not enough", "lacking")
    - Short response context dependency

Usage:
    python sentiment_analysis_validator.py

Output:
    - sentiment_comparison_report.xlsx - Full comparison of old vs new
    - validation_metrics.txt - Summary statistics
    - reclassification_examples.txt - Top 50 changes with explanations
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from datetime import datetime
from collections import Counter


# ============================================================================
# CONFIGURATION
# ============================================================================

# Question context mapping - defines sentiment bias for each question
QUESTION_CONTEXT = {
    # Negative bias - these questions ask about problems/pain points
    'challenges': ['What are the biggest challenges', 'operational challenges', 'biggest_challenges'],
    'stop_doing': ['What should we STOP doing', 'stop doing', 'STOP'],

    # Positive bias - these questions ask about strengths/initiatives
    'start_doing': ['What should we START doing', 'start doing', 'START'],
    'human_value': ['uniquely human', 'human value', 'humans'],
    'team_culture': ['How would you describe', 'team culture', 'describe our team'],

    # Neutral - informational questions
    'ai_tools': ['AI tools', 'currently using', 'tools you use'],
    'future_mission': ['future mission', '2 years', 'mission'],
}

# Gap/need indicator patterns - these indicate missing capabilities
GAP_PATTERNS = [
    r'\bmore\s+\w+',           # "more collaboration", "more support"
    r'\bbetter\s+\w+',         # "better communication", "better tools"
    r'\bneed\s+\w+',           # "need training", "need resources"
    r'\bneeds?\s+to\b',        # "needs to improve", "need to change"
    r'\bshould\s+\w+',         # "should focus", "should prioritize"
    r'\blacking\b',            # "lacking clarity"
    r'\bnot\s+enough\b',       # "not enough time"
    r'\binsufficient\b',       # "insufficient resources"
    r'\bwithout\b',            # "without proper support"
    r'\blisten\s+more\b',      # "listen more" (specific case)
    r'\bactive\s+listening\b', # "active listening" (specific case)
    r'\bimprove\s+\w+',        # "improve processes"
    r'\benhance\s+\w+',        # "enhance collaboration"
]

# Negation patterns - indicate problems or dissatisfaction
NEGATION_PATTERNS = [
    r'\bno\s+\w+',             # "no support", "no time"
    r'\bnot\b',                # "not working", "not effective"
    r'\bdon\'?t\b',            # "don't have", "dont know"
    r'\bcan\'?t\b',            # "can't access", "cant deliver"
    r'\bnever\b',              # "never enough"
    r'\bstop\b',               # "stop doing X"
    r'\bavoid\b',              # "avoid meetings"
]

# Pain point keywords - explicitly negative in business context
PAIN_KEYWORDS = [
    'challenge', 'problem', 'issue', 'struggle', 'difficult', 'hard',
    'frustrat', 'pain', 'blocker', 'obstacle', 'barrier', 'constraint',
    'overwork', 'stretch', 'burn', 'overwhelm', 'stress', 'complain',
    'incompetent', 'poor', 'bad', 'lack', 'miss', 'unavail', 'inadequate'
]

# Strength keywords - explicitly positive
STRENGTH_KEYWORDS = [
    'trust', 'empathy', 'connection', 'relationship', 'collaborat', 'support',
    'innovat', 'creative', 'expert', 'knowledge', 'skill', 'passion',
    'dedicated', 'commit', 'quality', 'excellent', 'strong', 'effective'
]


# ============================================================================
# SENTIMENT ANALYSIS FUNCTIONS
# ============================================================================

def preprocess_response(response):
    """
    Preprocess response text for better sentiment analysis.

    Handles:
    - Underscore-separated compound words (Team_work → team work)
    - Extra whitespace
    - Case normalization for pattern matching

    Args:
        response (str): Raw response text

    Returns:
        str: Cleaned response text
    """
    if pd.isna(response) or not isinstance(response, str):
        return ""

    # Replace underscores with spaces for compound words
    cleaned = response.replace('_', ' ')

    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())

    return cleaned


def detect_question_context(question_text):
    """
    Detect the context/bias of a question based on its text.

    Args:
        question_text (str): Full question text

    Returns:
        str: Context type ('negative_bias', 'positive_bias', 'neutral')
    """
    if pd.isna(question_text):
        return 'neutral'

    question_lower = question_text.lower()

    # Check for negative bias questions (challenges, pain points)
    for pattern in QUESTION_CONTEXT['challenges'] + QUESTION_CONTEXT['stop_doing']:
        if pattern.lower() in question_lower:
            return 'negative_bias'

    # Check for positive bias questions (strengths, initiatives)
    for pattern in QUESTION_CONTEXT['start_doing'] + QUESTION_CONTEXT['human_value']:
        if pattern.lower() in question_lower:
            return 'positive_bias'

    return 'neutral'


def detect_gap_indicators(response):
    """
    Detect if response contains gap/need indicators.

    These patterns suggest something is missing or insufficient,
    which should be classified as negative sentiment in survey context.

    Args:
        response (str): Response text

    Returns:
        bool: True if gap indicators detected
    """
    if not response:
        return False

    response_lower = response.lower()

    for pattern in GAP_PATTERNS:
        if re.search(pattern, response_lower):
            return True

    return False


def detect_negation(response):
    """
    Detect if response contains negation patterns.

    Args:
        response (str): Response text

    Returns:
        bool: True if negation detected
    """
    if not response:
        return False

    response_lower = response.lower()

    for pattern in NEGATION_PATTERNS:
        if re.search(pattern, response_lower):
            return True

    return False


def contains_keywords(response, keywords):
    """
    Check if response contains any keywords from a list.

    Args:
        response (str): Response text
        keywords (list): List of keyword patterns

    Returns:
        bool: True if any keyword found
    """
    if not response:
        return False

    response_lower = response.lower()

    for keyword in keywords:
        if keyword in response_lower:
            return True

    return False


def old_textblob_sentiment(response):
    """
    Original TextBlob-based sentiment analysis (current implementation).

    Uses simple polarity thresholds:
    - Positive: polarity > 0.1
    - Negative: polarity < -0.1
    - Neutral: -0.1 <= polarity <= 0.1

    Args:
        response (str): Response text

    Returns:
        tuple: (sentiment_label, polarity_score)
    """
    try:
        blob = TextBlob(str(response))
        polarity = blob.sentiment.polarity  # Range: -1.0 to +1.0

        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        return sentiment, polarity

    except Exception as e:
        return 'Neutral', 0.0


def new_contextual_sentiment(response, question_text, question_context):
    """
    NEW: Question-aware contextual sentiment analysis.

    Applies different logic based on:
    1. Question context (Q12/Q13 = negative bias, Q14 = positive bias)
    2. Gap/need indicators in response
    3. Negation patterns
    4. Pain point vs strength keywords
    5. Response length (short responses inherit question context)

    Args:
        response (str): Response text
        question_text (str): Full question text
        question_context (str): Detected context ('negative_bias', 'positive_bias', 'neutral')

    Returns:
        tuple: (sentiment_label, confidence_score, reasoning)
    """
    # Preprocess
    cleaned_response = preprocess_response(response)

    if not cleaned_response:
        return 'Neutral', 0.5, 'Empty response'

    # Get TextBlob baseline polarity
    try:
        blob = TextBlob(cleaned_response)
        base_polarity = blob.sentiment.polarity
    except:
        base_polarity = 0.0

    # Initialize decision factors
    reasoning_parts = []
    sentiment_score = base_polarity  # Start with TextBlob baseline
    confidence = 0.5

    # RULE 1: Question context bias
    if question_context == 'negative_bias':
        # Q12 (Challenges) or Q13 (Stop Doing) - default negative
        sentiment_score -= 0.4
        confidence = 0.8
        reasoning_parts.append(f"Question has negative context ({question_context})")

    elif question_context == 'positive_bias':
        # Q14 (Start Doing) or Q11 (Human Value) - default positive
        sentiment_score += 0.3
        confidence = 0.7
        reasoning_parts.append(f"Question has positive context ({question_context})")

    # RULE 2: Gap/need indicators override positive words
    if detect_gap_indicators(cleaned_response):
        sentiment_score -= 0.5
        confidence = 0.9
        reasoning_parts.append("Contains gap/need indicator (more/better/need/should)")

    # RULE 3: Negation patterns
    if detect_negation(cleaned_response):
        sentiment_score -= 0.4
        confidence = 0.85
        reasoning_parts.append("Contains negation pattern (no/not/stop/can't)")

    # RULE 4: Pain point keywords
    if contains_keywords(cleaned_response, PAIN_KEYWORDS):
        sentiment_score -= 0.3
        confidence = max(confidence, 0.8)
        reasoning_parts.append("Contains pain point keywords")

    # RULE 5: Strength keywords
    if contains_keywords(cleaned_response, STRENGTH_KEYWORDS):
        sentiment_score += 0.3
        confidence = max(confidence, 0.8)
        reasoning_parts.append("Contains strength keywords")

    # RULE 6: Short responses (1-3 words) inherit more question context
    word_count = len(cleaned_response.split())
    if word_count <= 3:
        if question_context == 'negative_bias':
            sentiment_score -= 0.2
            reasoning_parts.append("Short response in negative context")
        elif question_context == 'positive_bias':
            sentiment_score += 0.2
            reasoning_parts.append("Short response in positive context")

    # RULE 7: Specific edge cases
    response_lower = cleaned_response.lower()

    # "listen more", "active listening" → Negative (indicates gap)
    if 'listen' in response_lower and ('more' in response_lower or 'active' in response_lower):
        sentiment_score = -0.6
        confidence = 0.95
        reasoning_parts.append("Listening gap indicator (listen more/active listening)")

    # POC in "stop doing" context → Negative
    if 'poc' in response_lower and question_context == 'negative_bias':
        sentiment_score = -0.5
        confidence = 0.9
        reasoning_parts.append("POC in negative context (pain point)")

    # Final classification based on adjusted score
    if sentiment_score > 0.1:
        final_sentiment = 'Positive'
    elif sentiment_score < -0.1:
        final_sentiment = 'Negative'
    else:
        final_sentiment = 'Neutral'

    # Build reasoning summary
    if not reasoning_parts:
        reasoning_parts.append(f"TextBlob polarity: {base_polarity:.2f}")

    reasoning = '; '.join(reasoning_parts)

    return final_sentiment, confidence, reasoning


# ============================================================================
# DATA LOADING AND PROCESSING
# ============================================================================

def load_survey_data(file_path='raw-data.csv'):
    """
    Load survey data from CSV or Excel file.

    Args:
        file_path (str): Path to data file

    Returns:
        pd.DataFrame: Survey data with Question and Responses columns
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path, sheet_name='RawData')
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

        print(f"[OK] Loaded {len(df)} responses from {file_path}")
        return df

    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        print("\nTrying alternative data source...")

        # Try Excel workbook as backup
        try:
            df = pd.read_excel('presales_survey_analysis.xlsx', sheet_name='RawData')
            print(f"[OK] Loaded {len(df)} responses from Excel workbook")
            return df
        except:
            raise FileNotFoundError("Could not find raw-data.csv or presales_survey_analysis.xlsx")


def filter_open_ended_questions(df):
    """
    Filter to only open-ended questions (exclude multiple choice).

    Multiple choice questions have vote counts as responses (numbers),
    while open-ended have text responses.

    Args:
        df (pd.DataFrame): Survey data

    Returns:
        pd.DataFrame: Filtered data with only text responses
    """
    # Remove rows where Response is numeric (vote counts)
    df = df[df['Responses'].apply(lambda x: isinstance(x, str) and not str(x).isdigit())]

    print(f"[OK] Filtered to {len(df)} open-ended responses")
    return df


def run_dual_analysis(df):
    """
    Run both old (TextBlob) and new (Question-Aware) sentiment analysis
    on all responses.

    Args:
        df (pd.DataFrame): Survey data

    Returns:
        pd.DataFrame: Data with sentiment analysis columns added
    """
    results = []

    print("\nRunning dual sentiment analysis...")
    print(f"Total responses to analyze: {len(df)}")

    for idx, row in df.iterrows():
        question = row['Question']
        response = row['Responses']

        # Detect question context
        context = detect_question_context(question)

        # Run old method (TextBlob)
        old_sentiment, polarity = old_textblob_sentiment(response)

        # Run new method (Question-Aware)
        new_sentiment, confidence, reasoning = new_contextual_sentiment(
            response, question, context
        )

        # Check if sentiment changed
        changed = 'Yes' if old_sentiment != new_sentiment else 'No'

        results.append({
            'Question': question,
            'Response': response,
            'Question_Context': context,
            'Old_Sentiment': old_sentiment,
            'New_Sentiment': new_sentiment,
            'TextBlob_Polarity': polarity,
            'Confidence': confidence,
            'Changed': changed,
            'Reasoning': reasoning
        })

        # Progress indicator
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(df)} responses...")

    print(f"[OK] Analysis complete!")

    return pd.DataFrame(results)


# ============================================================================
# VALIDATION METRICS
# ============================================================================

def calculate_validation_metrics(results_df):
    """
    Calculate validation metrics comparing old vs new sentiment analysis.

    Metrics:
    - Total reclassifications
    - Reclassification rate by question
    - Sentiment distribution changes
    - Confidence distribution

    Args:
        results_df (pd.DataFrame): Results with both sentiment methods

    Returns:
        dict: Validation metrics
    """
    metrics = {}

    # Overall reclassification rate
    total_responses = len(results_df)
    changed_count = len(results_df[results_df['Changed'] == 'Yes'])
    metrics['total_responses'] = total_responses
    metrics['reclassifications'] = changed_count
    metrics['reclassification_rate'] = (changed_count / total_responses) * 100

    # Reclassification by question
    reclassification_by_q = results_df[results_df['Changed'] == 'Yes'].groupby('Question').size()
    metrics['reclassification_by_question'] = reclassification_by_q.to_dict()

    # Sentiment distribution changes
    old_dist = results_df['Old_Sentiment'].value_counts()
    new_dist = results_df['New_Sentiment'].value_counts()
    metrics['old_sentiment_distribution'] = old_dist.to_dict()
    metrics['new_sentiment_distribution'] = new_dist.to_dict()

    # Confidence distribution
    metrics['avg_confidence'] = results_df['Confidence'].mean()
    metrics['low_confidence_count'] = len(results_df[results_df['Confidence'] < 0.7])

    # Question context distribution
    context_dist = results_df['Question_Context'].value_counts()
    metrics['question_context_distribution'] = context_dist.to_dict()

    return metrics


def generate_metrics_report(metrics):
    """
    Generate human-readable metrics report.

    Args:
        metrics (dict): Validation metrics

    Returns:
        str: Formatted report text
    """
    report = []
    report.append("=" * 80)
    report.append("SENTIMENT ANALYSIS VALIDATION METRICS")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Overall statistics
    report.append("OVERALL STATISTICS")
    report.append("-" * 80)
    report.append(f"Total Responses Analyzed: {metrics['total_responses']}")
    report.append(f"Reclassifications: {metrics['reclassifications']}")
    report.append(f"Reclassification Rate: {metrics['reclassification_rate']:.1f}%")
    report.append(f"Average Confidence: {metrics['avg_confidence']:.2f}")
    report.append(f"Low Confidence (<0.7): {metrics['low_confidence_count']}")
    report.append("")

    # Sentiment distribution comparison
    report.append("SENTIMENT DISTRIBUTION COMPARISON")
    report.append("-" * 80)
    report.append("Old (TextBlob) Method:")
    for sentiment, count in sorted(metrics['old_sentiment_distribution'].items()):
        pct = (count / metrics['total_responses']) * 100
        report.append(f"  {sentiment}: {count} ({pct:.1f}%)")

    report.append("\nNew (Question-Aware) Method:")
    for sentiment, count in sorted(metrics['new_sentiment_distribution'].items()):
        pct = (count / metrics['total_responses']) * 100
        report.append(f"  {sentiment}: {count} ({pct:.1f}%)")
    report.append("")

    # Question context distribution
    report.append("QUESTION CONTEXT DISTRIBUTION")
    report.append("-" * 80)
    for context, count in sorted(metrics['question_context_distribution'].items()):
        pct = (count / metrics['total_responses']) * 100
        report.append(f"  {context}: {count} ({pct:.1f}%)")
    report.append("")

    # Top questions with most reclassifications
    report.append("TOP QUESTIONS BY RECLASSIFICATIONS")
    report.append("-" * 80)
    sorted_questions = sorted(
        metrics['reclassification_by_question'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    for question, count in sorted_questions:
        question_short = question[:60] + "..." if len(question) > 60 else question
        report.append(f"  {count:3d} changes | {question_short}")
    report.append("")

    report.append("=" * 80)

    return '\n'.join(report)


def generate_reclassification_examples(results_df, top_n=50):
    """
    Generate examples of reclassifications with explanations.

    Args:
        results_df (pd.DataFrame): Results with both sentiment methods
        top_n (int): Number of examples to include

    Returns:
        str: Formatted examples text
    """
    # Get changed responses
    changed = results_df[results_df['Changed'] == 'Yes'].copy()

    # Prioritize high-confidence changes
    changed = changed.sort_values('Confidence', ascending=False)

    examples = []
    examples.append("=" * 80)
    examples.append(f"TOP {top_n} RECLASSIFICATION EXAMPLES")
    examples.append("=" * 80)
    examples.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    examples.append("")

    for idx, row in changed.head(top_n).iterrows():
        examples.append("-" * 80)
        examples.append(f"Example {idx + 1}")
        examples.append("-" * 80)

        # Truncate question for readability
        question_short = row['Question'][:70] + "..." if len(row['Question']) > 70 else row['Question']
        examples.append(f"Question: {question_short}")
        examples.append(f"Response: \"{row['Response']}\"")
        examples.append(f"Question Context: {row['Question_Context']}")
        examples.append("")
        examples.append(f"Old Sentiment: {row['Old_Sentiment']} (TextBlob Polarity: {row['TextBlob_Polarity']:.2f})")
        examples.append(f"New Sentiment: {row['New_Sentiment']} (Confidence: {row['Confidence']:.2f})")
        examples.append(f"Reasoning: {row['Reasoning']}")
        examples.append("")

    examples.append("=" * 80)

    return '\n'.join(examples)


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_comparison_report(results_df, output_file='sentiment_comparison_report.xlsx'):
    """
    Export full comparison report to Excel with multiple sheets.

    Sheets:
    1. All_Results - Full dataset with all columns
    2. Changed_Only - Only reclassified responses
    3. Summary_Stats - Aggregated statistics

    Args:
        results_df (pd.DataFrame): Results with both sentiment methods
        output_file (str): Output file path
    """
    print(f"\nExporting comparison report to {output_file}...")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: All results
        results_df.to_excel(writer, sheet_name='All_Results', index=False)

        # Sheet 2: Changed only
        changed_df = results_df[results_df['Changed'] == 'Yes']
        changed_df.to_excel(writer, sheet_name='Changed_Only', index=False)

        # Sheet 3: Summary by question
        summary = results_df.groupby('Question').agg({
            'Response': 'count',
            'Changed': lambda x: (x == 'Yes').sum(),
            'Old_Sentiment': lambda x: x.value_counts().to_dict(),
            'New_Sentiment': lambda x: x.value_counts().to_dict(),
            'Confidence': 'mean'
        }).reset_index()
        summary.columns = ['Question', 'Total_Responses', 'Reclassifications',
                          'Old_Distribution', 'New_Distribution', 'Avg_Confidence']
        summary.to_excel(writer, sheet_name='Summary_By_Question', index=False)

        # Sheet 4: Low confidence responses for manual review
        low_confidence = results_df[results_df['Confidence'] < 0.7].sort_values('Confidence')
        low_confidence.to_excel(writer, sheet_name='Low_Confidence_Review', index=False)

    print(f"[OK] Exported {len(results_df)} results to {output_file}")
    print(f"  - All_Results: {len(results_df)} rows")
    print(f"  - Changed_Only: {len(changed_df)} rows")
    print(f"  - Summary_By_Question: {len(summary)} questions")
    print(f"  - Low_Confidence_Review: {len(low_confidence)} rows")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.

    Workflow:
    1. Load survey data
    2. Filter to open-ended questions
    3. Run dual sentiment analysis
    4. Calculate validation metrics
    5. Export reports
    """
    print("\n" + "=" * 80)
    print("SENTIMENT ANALYSIS VALIDATOR")
    print("=" * 80)
    print("\nValidating question-aware sentiment analysis vs. TextBlob baseline...")
    print("")

    # Step 1: Load data
    print("Step 1: Loading survey data...")
    df = load_survey_data('raw-data.csv')

    # Step 2: Filter to open-ended questions
    print("\nStep 2: Filtering to open-ended questions...")
    df = filter_open_ended_questions(df)

    # Step 3: Run dual analysis
    print("\nStep 3: Running dual sentiment analysis...")
    results_df = run_dual_analysis(df)

    # Step 4: Calculate metrics
    print("\nStep 4: Calculating validation metrics...")
    metrics = calculate_validation_metrics(results_df)

    # Step 5: Generate reports
    print("\nStep 5: Generating reports...")

    # Metrics report
    metrics_report = generate_metrics_report(metrics)
    with open('validation_metrics.txt', 'w', encoding='utf-8') as f:
        f.write(metrics_report)
    print("[OK] Saved validation_metrics.txt")

    # Reclassification examples
    examples_report = generate_reclassification_examples(results_df, top_n=50)
    with open('reclassification_examples.txt', 'w', encoding='utf-8') as f:
        f.write(examples_report)
    print("[OK] Saved reclassification_examples.txt")

    # Excel comparison report
    export_comparison_report(results_df)

    # Step 6: Display summary
    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print(f"\nTotal Responses: {metrics['total_responses']}")
    print(f"Reclassifications: {metrics['reclassifications']} ({metrics['reclassification_rate']:.1f}%)")
    print(f"Average Confidence: {metrics['avg_confidence']:.2f}")
    print(f"\nOutput Files:")
    print("  1. sentiment_comparison_report.xlsx - Full comparison with 4 sheets")
    print("  2. validation_metrics.txt - Summary statistics")
    print("  3. reclassification_examples.txt - Top 50 changes with explanations")
    print("\nNext Steps:")
    print("  1. Review sentiment_comparison_report.xlsx (Changed_Only sheet)")
    print("  2. Check reclassification_examples.txt for example improvements")
    print("  3. Review Low_Confidence_Review sheet for ambiguous cases")
    print("  4. If satisfied, integrate new sentiment engine into app.py")
    print("=" * 80)
    print("")


if __name__ == '__main__':
    main()
