"""
Automated Insight Generation for Presales Survey
Generates a comprehensive analysis report with key insights, frequencies, and cross-question patterns
"""

import pandas as pd
from collections import Counter
import re
from datetime import datetime

def clean_text(text):
    """Clean text for analysis"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_top_themes(responses, top_n=10, exclude_words=None):
    """Extract top N themes from responses"""
    if exclude_words is None:
        exclude_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                        'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                        'should', 'may', 'might', 'can', 'our', 'we', 'us', 'i', 'my', 'me',
                        'more', 'better', 'new', 'using', 'use', 'make', 'need'}

    all_words = []
    for response in responses:
        cleaned = clean_text(response)
        words = [w for w in cleaned.split() if w not in exclude_words and len(w) > 2]
        all_words.extend(words)

    word_counts = Counter(all_words)
    return word_counts.most_common(top_n)

def analyze_question(df, question_text, question_num):
    """Analyze a single question and return insights"""
    question_df = df[df['Question'].str.contains(question_text[:50], case=False, na=False)]

    if len(question_df) == 0:
        return None

    insights = {
        'number': question_num,
        'question': question_df['Question'].iloc[0],
        'total_responses': len(question_df),
        'unique_responses': question_df['Responses'].nunique(),
        'top_themes': get_top_themes(question_df['Responses'], top_n=15),
        'sample_responses': question_df['Responses'].head(5).tolist()
    }

    return insights

def generate_report(df):
    """Generate comprehensive insights report"""

    report = []
    report.append("=" * 80)
    report.append("PRESALES SURVEY - AUTOMATED INSIGHT REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Responses Analyzed: {len(df)}")
    report.append(f"Total Questions: {df['Question'].nunique()}")
    report.append("=" * 80)

    # Define question mapping
    question_map = [
        ("Team Culture", "How would you describe  the team culture"),
        ("Future Mission", "Looking 2 years ahead, what do you believe will be the primary mission"),
        ("Future Skills", "What do you believe are additional skillsets"),
        ("AI Use Cases", "How would you use AI to be more efficient"),
        ("AI Tools Current", "What AI Tools do you currently use"),
        ("Buyer Experience", "How should our team evolve the way we demonstrate value"),
        ("Success Outcomes", "What key outcomes should define success"),
        ("Team Relationships", "How should our team's relationship with Product Management"),
        ("Human Value", "what becomes the most important, uniquely human value"),
        ("Challenges", "What are your biggest challenges and internal bottlenecks"),
        ("Stop Doing", "What should we stop doing"),
        ("Start Doing", "What should we start doing differently"),
    ]

    insights_data = []

    for idx, (title, question_search) in enumerate(question_map, 1):
        insight = analyze_question(df, question_search, idx)
        if insight:
            insights_data.append(insight)

            report.append(f"\n{'=' * 80}")
            report.append(f"Q{idx}: {title}")
            report.append(f"{'=' * 80}")
            report.append(f"Full Question: {insight['question']}")
            report.append(f"Total Responses: {insight['total_responses']}")
            report.append(f"Unique Responses: {insight['unique_responses']}")

            report.append(f"\nTOP 15 THEMES (by frequency):")
            report.append("-" * 80)
            for rank, (theme, count) in enumerate(insight['top_themes'], 1):
                percentage = (count / insight['total_responses']) * 100
                report.append(f"  {rank:2d}. {theme:25s} - {count:3d} mentions ({percentage:5.1f}%)")

            report.append(f"\nSAMPLE RESPONSES:")
            report.append("-" * 80)
            for i, response in enumerate(insight['sample_responses'], 1):
                report.append(f"  {i}. \"{response}\"")

    # Cross-Question Analysis
    report.append(f"\n{'=' * 80}")
    report.append("CROSS-QUESTION INSIGHTS")
    report.append("=" * 80)

    # AI Gap Analysis
    report.append(f"\n[AI ADOPTION GAP ANALYSIS]")
    report.append("-" * 80)
    ai_use = analyze_question(df, "How would you use AI", None)
    ai_tools = analyze_question(df, "What AI Tools do you currently use", None)

    if ai_use and ai_tools:
        report.append(f"Desired AI Use Cases: {ai_use['total_responses']} responses")
        report.append(f"Current AI Tools: {ai_tools['total_responses']} responses")

        report.append(f"\nTop Desired Use Cases:")
        for theme, count in ai_use['top_themes'][:5]:
            report.append(f"  - {theme}: {count} mentions")

        report.append(f"\nTop Current Tools:")
        for theme, count in ai_tools['top_themes'][:5]:
            report.append(f"  - {theme}: {count} mentions")

    # Quick Wins Analysis
    report.append(f"\n[QUICK WINS ANALYSIS - High Frequency Items]")
    report.append("-" * 80)

    stop_doing = analyze_question(df, "What should we stop doing", None)
    start_doing = analyze_question(df, "What should we start doing", None)

    if stop_doing:
        report.append(f"\nSTOP DOING (Top Pain Points):")
        high_freq_stops = [(theme, count) for theme, count in stop_doing['top_themes']
                          if count >= stop_doing['total_responses'] * 0.05]  # 5% threshold
        for theme, count in high_freq_stops[:10]:
            percentage = (count / stop_doing['total_responses']) * 100
            report.append(f"  - {theme}: {count} mentions ({percentage:.1f}%) - PRIORITY")

    if start_doing:
        report.append(f"\nSTART DOING (Top Initiatives):")
        high_freq_starts = [(theme, count) for theme, count in start_doing['top_themes']
                           if count >= start_doing['total_responses'] * 0.05]
        for theme, count in high_freq_starts[:10]:
            percentage = (count / start_doing['total_responses']) * 100
            report.append(f"  - {theme}: {count} mentions ({percentage:.1f}%) - PRIORITY")

    # Strategic Tensions
    report.append(f"\n[STRATEGIC TENSIONS & PATTERNS]")
    report.append("-" * 80)

    mission = analyze_question(df, "Looking 2 years ahead", None)
    challenges = analyze_question(df, "biggest challenges", None)

    if mission and challenges:
        report.append(f"\nVision vs Reality Gap:")
        report.append(f"  Future Mission (Top themes): {', '.join([t[0] for t in mission['top_themes'][:5]])}")
        report.append(f"  Current Challenges (Top themes): {', '.join([t[0] for t in challenges['top_themes'][:5]])}")
        report.append(f"  >> Insight: Compare aspirational mission with operational reality")

    # Summary Recommendations
    report.append(f"\n{'=' * 80}")
    report.append("EXECUTIVE SUMMARY - KEY TAKEAWAYS")
    report.append("=" * 80)

    if stop_doing and start_doing:
        report.append(f"\n1. IMMEDIATE ACTIONS (0-30 days):")
        report.append(f"   Based on {stop_doing['total_responses'] + start_doing['total_responses']} responses")
        report.append(f"   - Top pain point to eliminate: {stop_doing['top_themes'][0][0]} ({stop_doing['top_themes'][0][1]} mentions)")
        report.append(f"   - Top initiative to launch: {start_doing['top_themes'][0][0]} ({start_doing['top_themes'][0][1]} mentions)")

    if ai_use and ai_tools:
        report.append(f"\n2. AI CAPABILITY GAP:")
        report.append(f"   - {ai_use['total_responses']} responses on desired AI use")
        report.append(f"   - {ai_tools['total_responses']} responses on current tools")
        report.append(f"   - Top opportunity: {ai_use['top_themes'][0][0]} (high demand, check adoption)")

    culture = analyze_question(df, "team culture", None)
    if culture:
        report.append(f"\n3. TEAM CULTURE:")
        report.append(f"   - Dominant theme: {culture['top_themes'][0][0]} ({culture['top_themes'][0][1]} mentions)")
        report.append(f"   - {culture['total_responses']} responses indicate team sentiment")

    report.append(f"\n{'=' * 80}")
    report.append("END OF REPORT")
    report.append("=" * 80)
    report.append("\nNext Steps:")
    report.append("1. Review high-frequency items (>5% mention rate) for quick wins")
    report.append("2. Use web app (streamlit run app.py) for visual exploration")
    report.append("3. Export key charts for executive presentation")
    report.append("4. Cross-reference this report with Executive_Summary_Template.md")

    return "\n".join(report)

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('raw-data.csv', encoding='utf-8-sig')
    df.columns = df.columns.str.strip()

    # Filter valid data
    df = df[df['Question'].notna() & (df['Question'] != 'nan')]
    df = df[df['Responses'].notna()]

    # Filter questions with substantial responses
    question_counts = df['Question'].value_counts()
    valid_questions = question_counts[question_counts >= 10].index
    df = df[df['Question'].isin(valid_questions)]

    # Generate report
    report = generate_report(df)

    # Save to file with timestamp
    timestamp_file = f"INSIGHTS_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(timestamp_file, 'w', encoding='utf-8') as f:
        f.write(report)

    # Also save to a fixed filename for easy access
    fixed_file = "INSIGHTS_REPORT_LATEST.txt"
    with open(fixed_file, 'w', encoding='utf-8') as f:
        f.write(report)

    output_file = timestamp_file  # For the print statement

    # Print summary only (avoid unicode issues)
    print("=" * 60)
    print("PRESALES SURVEY - INSIGHTS GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Report saved to: {output_file}")
    print(f"Also saved to: INSIGHTS_REPORT_LATEST.txt")
    print(f"Total responses analyzed: {len(df)}")
    print(f"Questions analyzed: {df['Question'].nunique()}")
    print("\nOpen the report file to view detailed insights.")
    print("=" * 60)
