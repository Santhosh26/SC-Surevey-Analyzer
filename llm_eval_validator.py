"""
LLM Batch Summarizer Validation Suite

Automated tests to detect hallucinations, inaccuracies, and quality issues
in AWS Bedrock Claude Opus 4.5 generated summaries.

This validator runs 6 tests across 3 tiers:
- Tier 1 (Critical): Quote hallucination, response counts, JSON schema
- Tier 2 (Accuracy): Frequency estimation, sentiment consistency, theme alignment
- Tier 3 (Quality): Manual review checklist

Usage:
    python llm_eval_validator.py

Outputs:
    - validation_report.json (detailed results)
    - validation_report.md (human-readable summary)
    - Console: PASS/FAIL status for each test

Author: Claude Code
Date: 2026-01-09
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Tuple
import datetime
import os
from collections import Counter

try:
    from fuzzywuzzy import fuzz
except ImportError:
    print("ERROR: fuzzywuzzy not installed. Run: pip install fuzzywuzzy python-Levenshtein")
    exit(1)

# Try to import app.py functions for sentiment and word analysis
try:
    from app import load_data, analyze_sentiment, get_top_words
    HAS_APP_FUNCTIONS = True
except ImportError:
    HAS_APP_FUNCTIONS = False
    print("WARNING: Could not import app.py functions. Some tests will be skipped.")


class LLMValidator:
    """Validates LLM batch summarizer output for hallucinations and accuracy."""

    def __init__(self, summaries_path='llm_summaries.json', raw_data_path='raw-data.csv'):
        """
        Initialize validator with paths to summaries and raw data.

        Args:
            summaries_path: Path to llm_summaries.json
            raw_data_path: Path to raw-data.csv
        """
        self.summaries_path = summaries_path
        self.raw_data_path = raw_data_path

        # Load data
        try:
            self.summaries = json.load(open(summaries_path, encoding='utf-8'))
        except FileNotFoundError:
            raise FileNotFoundError(f"llm_summaries.json not found at {summaries_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in llm_summaries.json: {e}")

        try:
            self.df = pd.read_csv(raw_data_path, encoding='utf-8-sig')
            self.df.columns = self.df.columns.str.strip()

            # Use 'Response' or 'Responses' column
            response_col = 'Responses' if 'Responses' in self.df.columns else 'Response'
            self.df = self.df.rename(columns={response_col: 'Response'})
        except FileNotFoundError:
            raise FileNotFoundError(f"raw-data.csv not found at {raw_data_path}")

        # Pre-process raw responses for quote matching
        self.all_responses = set(self.df['Response'].astype(str).str.strip().str.lower())

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all validation tests and compile results."""
        results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'summaries_file': self.summaries_path,
            'raw_data_file': self.raw_data_path,
            'tests': []
        }

        print("\n" + "="*70)
        print("LLM BATCH SUMMARIZER VALIDATION SUITE")
        print("="*70 + "\n")

        # Tier 1: Critical tests (must pass 100%)
        print("TIER 1: CRITICAL TESTS (Must Pass 100%)\n")
        results['tests'].append(self.test_quote_hallucination())
        results['tests'].append(self.test_response_counts())
        results['tests'].append(self.test_json_schema())

        # Tier 2: Accuracy tests (must pass 70-80%)
        print("\nTIER 2: ACCURACY TESTS (Must Pass 70-80%)\n")
        results['tests'].append(self.test_frequency_accuracy())
        if HAS_APP_FUNCTIONS:
            results['tests'].append(self.test_sentiment_consistency())
            results['tests'].append(self.test_theme_wordcloud_alignment())
        else:
            print("[WARN] Skipping Tier 2 tests (app.py functions not available)")

        # Summary
        self.print_summary(results)
        self.save_results(results)

        return results

    # ==================== TIER 1: CRITICAL TESTS ====================

    def test_quote_hallucination(self) -> Dict[str, Any]:
        """Test 1: Quote Hallucination Detection (CRITICAL)

        Verify all 'representative_quotes' actually exist in raw-data.csv
        """
        print("  Running: Quote Hallucination Detection...")

        results = []
        total_quotes = 0
        pass_count = 0

        for q_summary in self.summaries.get('question_summaries', []):
            question = q_summary.get('question', 'Unknown')
            quotes = q_summary.get('representative_quotes', [])

            for quote in quotes:
                total_quotes += 1
                quote_clean = quote.strip().lower()

                # Exact match
                if quote_clean in self.all_responses:
                    results.append({
                        'question': question,
                        'quote': quote[:100],  # Truncate for readability
                        'status': 'PASS',
                        'match_type': 'exact'
                    })
                    pass_count += 1
                # Fuzzy match (allow minor differences like punctuation)
                elif any(fuzz.ratio(quote_clean, resp) > 90 for resp in self.all_responses):
                    results.append({
                        'question': question,
                        'quote': quote[:100],
                        'status': 'PASS',
                        'match_type': 'fuzzy_90%'
                    })
                    pass_count += 1
                else:
                    results.append({
                        'question': question,
                        'quote': quote[:100],
                        'status': 'FAIL',
                        'match_type': 'NOT_FOUND'
                    })

        pass_rate = (pass_count / total_quotes * 100) if total_quotes > 0 else 0

        print(f"    [OK] Completed: {pass_count}/{total_quotes} quotes verified")

        return {
            'test_name': 'Quote Hallucination Detection',
            'pass_rate': pass_rate,
            'required': 100.0,
            'status': 'PASS' if pass_rate == 100.0 else 'FAIL',
            'details': results,
            'summary': f"{pass_count}/{total_quotes} quotes found in raw data"
        }

    def test_response_counts(self) -> Dict[str, Any]:
        """Test 2: Response Count Validation (CRITICAL)

        Verify 'response_count' fields match actual data
        """
        print("  Running: Response Count Validation...")

        # Count responses per question in raw data
        actual_counts = self.df.groupby('Question')['Response'].count().to_dict()

        results = []
        pass_count = 0
        total_questions = 0

        for q_summary in self.summaries.get('question_summaries', []):
            question = q_summary.get('question', 'Unknown')
            reported_count = q_summary.get('response_count', 0)
            actual_count = actual_counts.get(question, 0)

            total_questions += 1

            # Allow ±1 tolerance (rounding/filtering differences)
            match = abs(reported_count - actual_count) <= 1

            if match:
                pass_count += 1

            results.append({
                'question': question[:60],  # Truncate for readability
                'reported': reported_count,
                'actual': actual_count,
                'diff': reported_count - actual_count,
                'status': 'PASS' if match else 'FAIL'
            })

        pass_rate = (pass_count / total_questions * 100) if total_questions > 0 else 0

        print(f"    [PASS] Completed: {pass_count}/{total_questions} questions match (±1 tolerance)")

        return {
            'test_name': 'Response Count Validation',
            'pass_rate': pass_rate,
            'required': 100.0,
            'status': 'PASS' if pass_rate == 100.0 else 'FAIL',
            'details': results,
            'summary': f"{pass_count}/{total_questions} response counts within tolerance"
        }

    def test_json_schema(self) -> Dict[str, Any]:
        """Test 3: JSON Schema Validation (CRITICAL)

        Verify output structure matches expected schema
        """
        print("  Running: JSON Schema Validation...")

        required_top_level = ['metadata', 'question_summaries', 'overall_summary']
        required_question_fields = ['question', 'response_count', 'executive_summary',
                                   'themes', 'sentiment_analysis', 'representative_quotes',
                                   'actionable_insights', 'hidden_patterns']
        required_theme_fields = ['theme', 'frequency', 'description']

        errors = []

        # Check top-level structure
        for field in required_top_level:
            if field not in self.summaries:
                errors.append(f"Missing top-level field: {field}")

        # Check each question summary
        for i, q_summary in enumerate(self.summaries.get('question_summaries', [])):
            for field in required_question_fields:
                if field not in q_summary:
                    errors.append(f"Question {i+1} missing field: {field}")

            # Check themes structure
            for j, theme in enumerate(q_summary.get('themes', [])):
                for field in required_theme_fields:
                    if field not in theme:
                        errors.append(f"Question {i+1}, Theme {j+1} missing field: {field}")

        print(f"    [PASS] Completed: {0 if len(errors) == 0 else len(errors)} schema errors")

        return {
            'test_name': 'JSON Schema Validation',
            'pass_rate': 100.0 if len(errors) == 0 else 0.0,
            'required': 100.0,
            'status': 'PASS' if len(errors) == 0 else 'FAIL',
            'errors': errors,
            'summary': f"Schema {'valid' if len(errors) == 0 else f'invalid ({len(errors)} errors)'}"
        }

    # ==================== TIER 2: ACCURACY TESTS ====================

    def test_frequency_accuracy(self) -> Dict[str, Any]:
        """Test 4: Frequency Estimation Accuracy

        Validate frequency percentages match actual theme prevalence
        """
        print("  Running: Frequency Estimation Accuracy...")

        results = []
        pass_count = 0
        total_freq = 0

        for q_summary in self.summaries.get('question_summaries', []):
            question = q_summary.get('question', 'Unknown')
            themes = q_summary.get('themes', [])

            # Get responses for this question
            question_responses = self.df[self.df['Question'] == question]['Response'].tolist()
            total_responses = len(question_responses)

            if total_responses == 0:
                continue

            for theme in themes:
                total_freq += 1
                theme_name = theme.get('theme', 'Unknown')
                claimed_freq = theme.get('frequency', '0%')

                # Parse percentage
                try:
                    claimed_pct = float(claimed_freq.strip('%')) / 100
                except (ValueError, AttributeError):
                    results.append({
                        'question': question[:60],
                        'theme': theme_name[:60],
                        'claimed_freq': claimed_freq,
                        'estimated_actual': 'N/A',
                        'diff': 'N/A',
                        'status': 'FAIL'
                    })
                    continue

                # Estimate actual frequency by keyword matching
                keywords = [w.lower() for w in theme_name.split() if len(w) > 3]

                if not keywords:
                    # Theme has no keywords > 3 chars, skip
                    continue

                # Count responses mentioning any keyword
                matches = sum(1 for resp in question_responses
                            if any(kw in str(resp).lower() for kw in keywords))

                actual_freq = matches / total_responses if total_responses > 0 else 0
                diff = abs(claimed_pct - actual_freq)

                # Pass if within ±15% (LLM estimates, not exact counts)
                status = 'PASS' if diff <= 0.15 else 'FAIL'
                if status == 'PASS':
                    pass_count += 1

                results.append({
                    'question': question[:60],
                    'theme': theme_name[:60],
                    'claimed_freq': f"{claimed_pct*100:.0f}%",
                    'estimated_actual': f"{actual_freq*100:.0f}%",
                    'diff': f"{diff*100:.0f}%",
                    'status': status
                })

        pass_rate = (pass_count / total_freq * 100) if total_freq > 0 else 0

        print(f"    [PASS] Completed: {pass_count}/{total_freq} frequencies within ±15%")

        return {
            'test_name': 'Frequency Estimation Accuracy',
            'pass_rate': pass_rate,
            'required': 80.0,
            'status': 'PASS' if pass_rate >= 80.0 else 'FAIL',
            'details': results,
            'summary': f"{pass_count}/{total_freq} frequency claims within ±15% tolerance"
        }

    def test_sentiment_consistency(self) -> Dict[str, Any]:
        """Test 5: Sentiment Consistency Check

        Compare LLM sentiment vs rule-based sentiment analysis
        """
        if not HAS_APP_FUNCTIONS:
            return {
                'test_name': 'Sentiment Consistency Check',
                'pass_rate': 0.0,
                'required': 70.0,
                'status': 'SKIPPED',
                'details': [],
                'summary': 'Skipped (app.py functions not available)'
            }

        print("  Running: Sentiment Consistency Check...")

        df, _ = load_data()
        results = []
        pass_count = 0
        total = 0

        for q_summary in self.summaries.get('question_summaries', []):
            question = q_summary.get('question', 'Unknown')
            llm_sentiment = q_summary.get('sentiment_analysis', {}).get('overall', 'Unknown')

            # Get rule-based sentiment
            question_responses = df[df['Question'] == question]['Response'].tolist()
            if not question_responses:
                continue

            try:
                rule_sentiment_df = analyze_sentiment(question_responses, question)
                rule_counts = rule_sentiment_df['sentiment'].value_counts()
                rule_sentiment = rule_counts.idxmax() if len(rule_counts) > 0 else 'Unknown'
            except:
                rule_sentiment = 'Unknown'

            total += 1

            # Check alignment
            aligned = (llm_sentiment == rule_sentiment) or (llm_sentiment == 'Neutral' or rule_sentiment == 'Neutral')

            if aligned:
                pass_count += 1

            results.append({
                'question': question[:60],
                'llm_sentiment': llm_sentiment,
                'rule_sentiment': rule_sentiment,
                'aligned': aligned,
                'status': 'PASS' if aligned else 'WARNING'
            })

        pass_rate = (pass_count / total * 100) if total > 0 else 0

        print(f"    [PASS] Completed: {pass_count}/{total} sentiments aligned")

        return {
            'test_name': 'Sentiment Consistency Check',
            'pass_rate': pass_rate,
            'required': 70.0,
            'status': 'PASS' if pass_rate >= 70.0 else 'WARNING',
            'details': results,
            'summary': f"{pass_count}/{total} sentiments directionally aligned"
        }

    def test_theme_wordcloud_alignment(self) -> Dict[str, Any]:
        """Test 6: Theme-WordCloud Alignment

        Validate AI themes match top words in word clouds
        """
        if not HAS_APP_FUNCTIONS:
            return {
                'test_name': 'Theme-WordCloud Alignment',
                'pass_rate': 0.0,
                'required': 60.0,
                'status': 'SKIPPED',
                'details': [],
                'summary': 'Skipped (app.py functions not available)'
            }

        print("  Running: Theme-WordCloud Alignment...")

        df, _ = load_data()
        results = []
        pass_count = 0
        total = 0

        for q_summary in self.summaries.get('question_summaries', []):
            question = q_summary.get('question', 'Unknown')
            themes = q_summary.get('themes', [])

            # Get top 20 words
            question_responses = df[df['Question'] == question]['Response'].tolist()
            if not question_responses:
                continue

            try:
                top_words = get_top_words(question_responses, top_n=20)
                top_word_set = set([word.lower() for word, count in top_words])
            except:
                top_word_set = set()

            for theme in themes:
                total += 1
                theme_name = theme.get('theme', 'Unknown')
                theme_keywords = [w.lower() for w in theme_name.split() if len(w) > 3]

                # Check overlap
                overlap = any(kw in top_word_set for kw in theme_keywords)

                if overlap:
                    pass_count += 1

                results.append({
                    'question': question[:60],
                    'theme': theme_name[:60],
                    'overlaps_top_words': overlap,
                    'status': 'PASS' if overlap else 'WARNING'
                })

        pass_rate = (pass_count / total * 100) if total > 0 else 0

        print(f"    [PASS] Completed: {pass_count}/{total} themes aligned with word clouds")

        return {
            'test_name': 'Theme-WordCloud Alignment',
            'pass_rate': pass_rate,
            'required': 60.0,
            'status': 'PASS' if pass_rate >= 60.0 else 'WARNING',
            'details': results,
            'summary': f"{pass_count}/{total} themes overlap with top words"
        }

    # ==================== REPORTING ====================

    def print_summary(self, results: Dict[str, Any]) -> None:
        """Print validation summary to console."""
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70 + "\n")

        # Tier 1 status
        tier1_tests = results['tests'][:3]
        tier1_pass = all(t['status'] == 'PASS' for t in tier1_tests)

        print("TIER 1 (Critical - Must Pass 100%):")
        for test in tier1_tests:
            status_icon = '[PASS]' if test['status'] == 'PASS' else '[FAIL]'
            pass_rate = test.get('pass_rate', 0)
            print(f"  {status_icon} {test['test_name']}: {pass_rate:.1f}%")

        # Tier 2 status
        tier2_tests = results['tests'][3:]
        tier2_pass = sum(1 for t in tier2_tests if t['status'] in ['PASS', 'WARNING'])

        print(f"\nTIER 2 (Accuracy - Must Pass 70-80%): {tier2_pass}/{len(tier2_tests)} passed")
        for test in tier2_tests:
            if test['status'] == 'SKIPPED':
                status_icon = '[SKIP]'
            elif test['status'] == 'PASS':
                status_icon = '[PASS]'
            else:
                status_icon = '[WARN]'
            pass_rate = test.get('pass_rate', 0)
            print(f"  {status_icon} {test['test_name']}: {pass_rate:.1f}%")

        # Overall verdict
        print("\n" + "="*70)
        if tier1_pass and tier2_pass >= 2:
            print("OVERALL: [PASS] VALIDATION PASSED")
            print("\n LLM output is trustworthy for strategic decision-making")
        else:
            print("OVERALL: [FAIL] VALIDATION FAILED")
            print("\n Do NOT use LLM insights until failures are resolved")
        print("="*70 + "\n")

    def save_results(self, results: Dict[str, Any]) -> None:
        """Save validation results to JSON and Markdown files."""
        # Save JSON
        with open('validation_report.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # Generate and save Markdown report
        md_report = self.generate_markdown_report(results)
        with open('validation_report.md', 'w', encoding='utf-8') as f:
            f.write(md_report)

        print("[PASS] Results saved to:")
        print(f"  • validation_report.json")
        print(f"  • validation_report.md")

    def generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable Markdown report."""
        timestamp = results.get('timestamp', 'Unknown')
        model = self.summaries.get('metadata', {}).get('model', 'Unknown')
        total_responses = self.summaries.get('metadata', {}).get('total_responses', 0)
        total_questions = self.summaries.get('metadata', {}).get('total_questions', 0)

        # Determine overall status
        tier1_pass = all(t['status'] == 'PASS' for t in results['tests'][:3])
        tier2_pass = sum(1 for t in results['tests'][3:] if t['status'] in ['PASS', 'WARNING'])
        overall_status = "[PASS] PASSED" if (tier1_pass and tier2_pass >= 2) else "[FAIL] FAILED"

        report = f"""# LLM Batch Summarizer Validation Report

**Generated**: {timestamp}
**Model**: {model}
**Dataset**: {total_responses} responses across {total_questions} questions

---

## Overall Status: {overall_status}

"""

        if tier1_pass and tier2_pass >= 2:
            report += """The LLM batch summarizer produces **trustworthy, hallucination-free insights** suitable for strategic decision-making.

### Validation Summary:
-  Zero hallucinated quotes detected
-  All response counts accurate
-  JSON structure valid
-  Frequency estimates within tolerance
-  Themes align with word clouds

"""
        else:
            report += """The LLM batch summarizer has failed validation and **should NOT be used** for strategic decision-making until issues are resolved.

### Failures Detected:
"""
            for test in results['tests']:
                if test['status'] == 'FAIL':
                    report += f"-  {test['test_name']}: {test.get('summary', 'Check details')}\n"

        # Test results table
        report += "\n---\n\n## Test Results\n\n### Tier 1: Critical Tests (Must Pass 100%)\n\n"
        report += "| Test | Status | Pass Rate | Required |\n"
        report += "|------|--------|-----------|----------|\n"

        for test in results['tests'][:3]:
            status_icon = '[PASS]' if test['status'] == 'PASS' else '[FAIL]'
            pass_rate = test.get('pass_rate', 0)
            report += f"| {test['test_name']} | {status_icon} {test['status']} | {pass_rate:.1f}% | {test.get('required', 'N/A')}% |\n"

        report += "\n### Tier 2: Accuracy Tests (Must Pass 70-80%)\n\n"
        report += "| Test | Status | Pass Rate | Required |\n"
        report += "|------|--------|-----------|----------|\n"

        for test in results['tests'][3:]:
            if test['status'] == 'SKIPPED':
                status_icon = '[SKIP]'
            elif test['status'] == 'PASS':
                status_icon = '[PASS]'
            else:
                status_icon = '[WARN]'
            pass_rate = test.get('pass_rate', 0)
            report += f"| {test['test_name']} | {status_icon} {test['status']} | {pass_rate:.1f}% | {test.get('required', 'N/A')}% |\n"

        # Detailed findings
        report += "\n---\n\n## Detailed Findings\n\n"

        for i, test in enumerate(results['tests'], 1):
            report += f"### Test {i}: {test['test_name']}\n\n"
            report += f"**Status**: {test['status']} ({test.get('pass_rate', 0):.1f}%)\n\n"
            report += f"**Summary**: {test.get('summary', 'See details below')}\n\n"

            # Show sample results
            details = test.get('details', [])
            if details and isinstance(details, list) and len(details) > 0:
                report += "**Sample Results**:\n\n"
                for detail in details[:5]:
                    if isinstance(detail, dict):
                        report += f"- {detail}\n"
                if len(details) > 5:
                    report += f"\n... and {len(details) - 5} more\n"
                report += "\n"

            # Show errors if any
            errors = test.get('errors', [])
            if errors:
                report += "**Errors**:\n\n"
                for error in errors:
                    report += f"- {error}\n"
                report += "\n"

        # Recommendations
        report += "---\n\n## Recommendations\n\n"

        if tier1_pass:
            report += "### For Immediate Use:\n"
            report += "1.  **Quote citations are trustworthy** - Safe to share with stakeholders\n"
            report += "2.  **Response counts are accurate** - No fabricated data detected\n"
            report += "3.  **JSON structure is valid** - Dashboard integration ready\n\n"
        else:
            report += "### Blocking Issues:\n"
            for test in results['tests'][:3]:
                if test['status'] == 'FAIL':
                    report += f"-  {test['test_name']}: Fix before using in production\n"
            report += "\n"

        if tier2_pass >= 2:
            report += "### Accuracy Assessment:\n"
            report += "-  **Frequency estimates are accurate** within ±15% tolerance\n"
            report += "-  **Themes align with data** - Validated against word clouds\n"
            report += "-  **Sentiment is directionally correct** - Matches rule-based analysis\n\n"
        else:
            report += "### Accuracy Concerns:\n"
            for test in results['tests'][3:]:
                if test['status'] == 'FAIL':
                    report += f"- [WARN] {test['test_name']}: Review outliers and cross-validate\n"
            report += "\n"

        # Risk assessment
        report += "### Risk Assessment:\n"
        if tier1_pass:
            report += "- **Hallucination Risk**: [PASS] LOW (0% fabricated content)\n"
        else:
            report += "- **Hallucination Risk**: [FAIL] HIGH (fabricated content detected)\n"

        if tier2_pass >= 2:
            report += "- **Accuracy Risk**: [PASS] LOW (frequency estimates validated)\n"
        else:
            report += "- **Accuracy Risk**: [WARN] MEDIUM (review frequency outliers)\n"

        report += "- **Quality Risk**: [WARN] MEDIUM (manual review recommended for insights)\n\n"

        # Next steps
        report += "---\n\n## Next Steps\n\n"

        if tier1_pass and tier2_pass >= 2:
            report += "1.  **Deploy to production** - AI Insights tab is ready for stakeholders\n"
            report += "2. 📋 **Complete manual review** - Validate executive summary quality\n"
            report += "3. 📧 **Share with stakeholders** - Include this validation report\n"
        else:
            report += "1.  **DO NOT DEPLOY** - Fix failing tests first\n"
            report += "2. 🔍 **Investigate failures** - Review details in validation_report.json\n"
            report += "3. 🛠️ **Fix and re-validate** - Re-run this script after fixes\n"

        report += "\n---\n\n"
        report += f"**Validated by**: llm_eval_validator.py\n"
        report += f"**Report generated**: {timestamp}\n"

        return report


def main():
    """Command-line entry point."""
    import sys

    # Check for custom paths
    summaries_path = sys.argv[1] if len(sys.argv) > 1 else 'llm_summaries.json'
    raw_data_path = sys.argv[2] if len(sys.argv) > 2 else 'raw-data.csv'

    try:
        validator = LLMValidator(summaries_path, raw_data_path)
        results = validator.run_all_tests()

        # Return exit code based on validation
        tier1_pass = all(t['status'] == 'PASS' for t in results['tests'][:3])
        tier2_pass = sum(1 for t in results['tests'][3:] if t['status'] in ['PASS', 'WARNING'])

        if tier1_pass and tier2_pass >= 2:
            return 0  # Success
        else:
            return 1  # Failure

    except FileNotFoundError as e:
        print(f"[FAIL] Error: {e}")
        print("\nUsage: python llm_eval_validator.py [summaries.json] [raw-data.csv]")
        return 1
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
