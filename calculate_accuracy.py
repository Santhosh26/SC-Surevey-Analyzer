"""
Accuracy Calculator for Sentiment Analysis Validation
======================================================

This script calculates accuracy metrics by comparing sentiment predictions
against manually labeled ground truth.

Usage:
    1. Open ground_truth_sample.csv
    2. Fill in the "Your_Label" column with correct sentiment (Positive/Neutral/Negative)
    3. Run: python calculate_accuracy.py
    4. Review accuracy metrics for old vs new sentiment analysis

Output:
    - Accuracy scores for old method
    - Accuracy scores for new method
    - Confusion matrix
    - Examples of correct/incorrect classifications
"""

import pandas as pd
import numpy as np
from collections import Counter


def calculate_accuracy(ground_truth_df):
    """
    Calculate accuracy metrics comparing predictions to ground truth.

    Args:
        ground_truth_df (pd.DataFrame): DataFrame with columns:
            - Old_Sentiment
            - New_Sentiment
            - Your_Label (ground truth)

    Returns:
        dict: Accuracy metrics
    """
    # Filter to only labeled responses
    labeled = ground_truth_df[ground_truth_df['Your_Label'].notna()].copy()

    if len(labeled) == 0:
        print("\n[ERROR] No labeled responses found in 'Your_Label' column!")
        print("Please fill in the 'Your_Label' column in ground_truth_sample.csv")
        print("Valid values: Positive, Neutral, Negative")
        return None

    print(f"\n[OK] Found {len(labeled)} labeled responses for validation")

    # Calculate accuracy for old method
    old_correct = (labeled['Old_Sentiment'] == labeled['Your_Label']).sum()
    old_accuracy = (old_correct / len(labeled)) * 100

    # Calculate accuracy for new method
    new_correct = (labeled['New_Sentiment'] == labeled['Your_Label']).sum()
    new_accuracy = (new_correct / len(labeled)) * 100

    # Improvement
    improvement = new_accuracy - old_accuracy

    metrics = {
        'total_labeled': len(labeled),
        'old_correct': old_correct,
        'old_accuracy': old_accuracy,
        'new_correct': new_correct,
        'new_accuracy': new_accuracy,
        'improvement': improvement
    }

    return metrics, labeled


def generate_confusion_matrix(predictions, ground_truth):
    """
    Generate confusion matrix for sentiment predictions.

    Args:
        predictions (pd.Series): Predicted sentiments
        ground_truth (pd.Series): Ground truth labels

    Returns:
        pd.DataFrame: Confusion matrix
    """
    labels = ['Positive', 'Neutral', 'Negative']

    # Create confusion matrix
    confusion = pd.DataFrame(0, index=labels, columns=labels)

    for pred, truth in zip(predictions, ground_truth):
        if pred in labels and truth in labels:
            confusion.loc[truth, pred] += 1

    return confusion


def generate_report(metrics, labeled_df):
    """
    Generate comprehensive accuracy report.

    Args:
        metrics (dict): Accuracy metrics
        labeled_df (pd.DataFrame): Labeled responses

    Returns:
        str: Formatted report
    """
    report = []
    report.append("=" * 80)
    report.append("SENTIMENT ANALYSIS ACCURACY VALIDATION")
    report.append("=" * 80)
    report.append("")

    # Overall accuracy
    report.append("OVERALL ACCURACY")
    report.append("-" * 80)
    report.append(f"Total Labeled Responses: {metrics['total_labeled']}")
    report.append("")
    report.append(f"Old Method (TextBlob):")
    report.append(f"  Correct: {metrics['old_correct']} / {metrics['total_labeled']}")
    report.append(f"  Accuracy: {metrics['old_accuracy']:.1f}%")
    report.append("")
    report.append(f"New Method (Question-Aware):")
    report.append(f"  Correct: {metrics['new_correct']} / {metrics['total_labeled']}")
    report.append(f"  Accuracy: {metrics['new_accuracy']:.1f}%")
    report.append("")
    report.append(f"IMPROVEMENT: {metrics['improvement']:+.1f}%")
    report.append("")

    # Confusion matrices
    report.append("CONFUSION MATRIX - OLD METHOD (TextBlob)")
    report.append("-" * 80)
    old_confusion = generate_confusion_matrix(labeled_df['Old_Sentiment'], labeled_df['Your_Label'])
    report.append("Predicted →")
    report.append(old_confusion.to_string())
    report.append("↑ Actual (Ground Truth)")
    report.append("")

    report.append("CONFUSION MATRIX - NEW METHOD (Question-Aware)")
    report.append("-" * 80)
    new_confusion = generate_confusion_matrix(labeled_df['New_Sentiment'], labeled_df['Your_Label'])
    report.append("Predicted →")
    report.append(new_confusion.to_string())
    report.append("↑ Actual (Ground Truth)")
    report.append("")

    # Per-sentiment accuracy
    report.append("ACCURACY BY SENTIMENT CLASS")
    report.append("-" * 80)

    for sentiment in ['Positive', 'Neutral', 'Negative']:
        subset = labeled_df[labeled_df['Your_Label'] == sentiment]
        if len(subset) == 0:
            continue

        old_correct = (subset['Old_Sentiment'] == sentiment).sum()
        new_correct = (subset['New_Sentiment'] == sentiment).sum()

        old_acc = (old_correct / len(subset)) * 100
        new_acc = (new_correct / len(subset)) * 100

        report.append(f"{sentiment}:")
        report.append(f"  Total: {len(subset)}")
        report.append(f"  Old Accuracy: {old_acc:.1f}% ({old_correct}/{len(subset)})")
        report.append(f"  New Accuracy: {new_acc:.1f}% ({new_correct}/{len(subset)})")
        report.append(f"  Improvement: {new_acc - old_acc:+.1f}%")
        report.append("")

    # Examples of improvements
    report.append("EXAMPLES OF IMPROVEMENTS (New Correct, Old Incorrect)")
    report.append("-" * 80)

    improvements = labeled_df[
        (labeled_df['New_Sentiment'] == labeled_df['Your_Label']) &
        (labeled_df['Old_Sentiment'] != labeled_df['Your_Label'])
    ]

    if len(improvements) > 0:
        for idx, row in improvements.head(10).iterrows():
            report.append(f"Response: \"{row['Response']}\"")
            report.append(f"  Ground Truth: {row['Your_Label']}")
            report.append(f"  Old: {row['Old_Sentiment']} (WRONG)")
            report.append(f"  New: {row['New_Sentiment']} (CORRECT)")
            report.append("")
    else:
        report.append("  (No improvements found)")
        report.append("")

    # Examples of regressions
    report.append("EXAMPLES OF REGRESSIONS (New Incorrect, Old Correct)")
    report.append("-" * 80)

    regressions = labeled_df[
        (labeled_df['Old_Sentiment'] == labeled_df['Your_Label']) &
        (labeled_df['New_Sentiment'] != labeled_df['Your_Label'])
    ]

    if len(regressions) > 0:
        for idx, row in regressions.head(10).iterrows():
            report.append(f"Response: \"{row['Response']}\"")
            report.append(f"  Ground Truth: {row['Your_Label']}")
            report.append(f"  Old: {row['Old_Sentiment']} (CORRECT)")
            report.append(f"  New: {row['New_Sentiment']} (WRONG)")
            report.append("")
    else:
        report.append("  (No regressions found - perfect!)")
        report.append("")

    report.append("=" * 80)

    return '\n'.join(report)


def main():
    """
    Main execution function.
    """
    print("\n" + "=" * 80)
    print("SENTIMENT ANALYSIS ACCURACY CALCULATOR")
    print("=" * 80)

    # Load ground truth
    try:
        df = pd.read_csv('ground_truth_sample.csv')
        print(f"[OK] Loaded ground_truth_sample.csv ({len(df)} responses)")
    except FileNotFoundError:
        print("[ERROR] ground_truth_sample.csv not found!")
        print("Please ensure the file exists in the current directory.")
        return

    # Calculate metrics
    result = calculate_accuracy(df)

    if result is None:
        return

    metrics, labeled_df = result

    # Generate report
    report = generate_report(metrics, labeled_df)

    # Display to console
    print("\n" + report)

    # Save to file
    with open('accuracy_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\n[OK] Saved accuracy_report.txt")
    print("\n" + "=" * 80)
    print(f"\nSUMMARY:")
    print(f"  Old Accuracy: {metrics['old_accuracy']:.1f}%")
    print(f"  New Accuracy: {metrics['new_accuracy']:.1f}%")
    print(f"  Improvement: {metrics['improvement']:+.1f}%")
    print("\n" + "=" * 80)


if __name__ == '__main__':
    main()
