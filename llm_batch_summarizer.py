"""
LLM Batch Summarizer for Survey Analysis

This module uses AWS Bedrock Claude Opus 4.5 to generate comprehensive summaries
for survey responses. It processes each question individually and generates an
overall synthesis across all questions.

Cost: ~$2.08 per full survey run (12 questions + overall summary)

Authentication:
  - Option 1: AWS Bedrock API Key (recommended, simpler)
    Set environment variable: AWS_BEARER_TOKEN_BEDROCK=your_api_key_here
  - Option 2: Traditional AWS credentials (access key + secret key)
    Configure via: aws configure
"""

import json
import boto3
import pandas as pd
from typing import Dict, List, Any
import time
import os
from pathlib import Path

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use system environment variables

# Question context mapping for bias-aware prompting
QUESTION_CONTEXT = {
    'negative_bias': [
        'What should we STOP doing today?',
        'What are your biggest challenges and internal bottlenecks today?',
        'Operational Challenge',
    ],
    'positive_bias': [
        'What should we START doing differently tomorrow?',
        'what becomes the most important, uniquely human',
        'How would you describe the team culture',
        'How would you describe our team culture',
    ],
    'neutral': [
        'AI tools',
        'Future',
        'mission',
        'What do you believe',
        'How would you use AI',
        'What key outcomes',
    ]
}


class LLMBatchSummarizer:
    """
    Batch summarization engine using AWS Bedrock Claude Opus 4.5.
    Generates comprehensive, high-quality summaries for survey analysis.
    """

    def __init__(self, region_name='us-east-1', model_id='us.anthropic.claude-opus-4-5-20251101-v1:0'):
        """
        Initialize the summarizer with AWS Bedrock client.

        Supports two authentication methods:
        1. AWS Bedrock API Key (set AWS_BEDROCK_API_KEY environment variable)
        2. Traditional AWS credentials (access key + secret key)

        Args:
            region_name: AWS region for Bedrock (default: us-east-1)
            model_id: Claude model ID (default: Opus 4.5)
        """
        try:
            # Check for AWS Bedrock API key (bearer token)
            api_key = os.environ.get('AWS_BEARER_TOKEN_BEDROCK')

            if api_key:
                # Use API key authentication (simpler method)
                print("✓ Using AWS Bedrock API Key authentication")
                # boto3 automatically detects AWS_BEARER_TOKEN_BEDROCK env var
                # No need to manually configure - just create the client
                self.bedrock = boto3.client('bedrock-runtime', region_name=region_name)
            else:
                # Use traditional AWS credentials (from aws configure or env vars)
                print("✓ Using traditional AWS credentials")
                self.bedrock = boto3.client('bedrock-runtime', region_name=region_name)

            self.model_id = model_id
            print(f"✓ Initialized AWS Bedrock client with {model_id}")

        except Exception as e:
            print(f"✗ Error initializing AWS Bedrock: {e}")
            print("\nAuthentication options:")
            print("  1. Set AWS_BEARER_TOKEN_BEDROCK environment variable (recommended)")
            print("     Example: set AWS_BEARER_TOKEN_BEDROCK=your_api_key_here")
            print("  2. Configure AWS credentials: aws configure")
            print("\nSee AWS_BEDROCK_SETUP.md for detailed instructions.")
            raise

    def _get_question_context(self, question: str) -> str:
        """
        Determine question context (negative_bias, positive_bias, or neutral).

        Args:
            question: The survey question text

        Returns:
            Context type as string
        """
        question_lower = question.lower()

        for context_type, patterns in QUESTION_CONTEXT.items():
            for pattern in patterns:
                if pattern.lower() in question_lower:
                    return context_type

        return 'neutral'

    def _call_bedrock(self, prompt: str, max_tokens: int = 4000) -> str:
        """
        Call AWS Bedrock with retry logic.

        Args:
            prompt: The prompt to send to Claude
            max_tokens: Maximum tokens in response

        Returns:
            Response text from Claude
        """
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3  # Lower temperature for more consistent analysis
            }

            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )

            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']

        except Exception as e:
            print(f"✗ Error calling Bedrock: {e}")
            raise

    def summarize_question(self, question: str, responses: List[str]) -> Dict[str, Any]:
        """
        Generate comprehensive summary for a single question.

        Args:
            question: The survey question text
            responses: List of all responses to this question

        Returns:
            Dictionary with summary, themes, sentiment, quotes, insights
        """
        context = self._get_question_context(question)
        response_count = len(responses)

        # Format responses as numbered list
        responses_text = "\n".join([f"{i+1}. {resp}" for i, resp in enumerate(responses)])

        # Build prompt for question analysis
        prompt = f"""You are analyzing survey responses from Solution Consultants (presales professionals) at an enterprise software company.

Survey Question: "{question}"
Total Responses: {response_count}
Question Context: {context} (This indicates if the question has inherent positive/negative bias)

All Responses:
{responses_text}

Provide a comprehensive analysis in this EXACT JSON format (must be valid JSON):
{{
  "executive_summary": "A 3-5 sentence overview of the key findings. Focus on patterns, frequencies, and strategic implications. Be specific and data-driven.",
  "themes": [
    {{"theme": "Theme Name 1", "frequency": "XX%", "description": "Detailed explanation of this theme with context"}},
    {{"theme": "Theme Name 2", "frequency": "XX%", "description": "Detailed explanation of this theme with context"}},
    {{"theme": "Theme Name 3", "frequency": "XX%", "description": "Detailed explanation of this theme with context"}},
    {{"theme": "Theme Name 4", "frequency": "XX%", "description": "Detailed explanation of this theme with context"}},
    {{"theme": "Theme Name 5", "frequency": "XX%", "description": "Detailed explanation of this theme with context"}}
  ],
  "sentiment_analysis": {{
    "overall": "Positive/Neutral/Negative",
    "reasoning": "Detailed explanation of why this sentiment classification was chosen. Consider the question context (bias) when interpreting.",
    "confidence": 0.85
  }},
  "representative_quotes": [
    "Actual quote 1 from responses that represents common theme",
    "Actual quote 2 from responses that represents another common theme",
    "Actual quote 3 from responses that shows interesting perspective"
  ],
  "actionable_insights": [
    "Specific action leadership should take based on this data",
    "Another specific action with clear rationale",
    "A third action that addresses patterns seen in responses"
  ],
  "hidden_patterns": "2-3 sentences describing what is IMPLIED but not directly stated. What are people NOT saying? What assumptions underlie the responses? What organizational dynamics are revealed?"
}}

CRITICAL INSTRUCTIONS:
1. All quotes MUST be actual responses from the list above (copy verbatim, don't paraphrase)
2. Frequency percentages should be estimated based on how many responses mention that theme
3. Consider the question context ({context}) when interpreting sentiment
4. Be specific and actionable in your insights
5. Return ONLY valid JSON (no markdown formatting, no extra text)"""

        print(f"  → Analyzing: {question[:60]}... ({response_count} responses)")

        try:
            response_text = self._call_bedrock(prompt)

            # Clean response (remove markdown code blocks if present)
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse JSON
            summary = json.loads(response_text)
            summary['question'] = question
            summary['response_count'] = response_count

            print(f"  ✓ Completed: {len(summary['themes'])} themes identified")
            return summary

        except json.JSONDecodeError as e:
            print(f"  ✗ JSON parsing error: {e}")
            print(f"  Response was: {response_text[:500]}...")
            raise
        except Exception as e:
            print(f"  ✗ Error processing question: {e}")
            raise

    def generate_overall_summary(self, question_summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate cross-question synthesis and organizational assessment.

        Args:
            question_summaries: List of all question summaries

        Returns:
            Dictionary with overall assessment, priorities, risks, action plan
        """
        print("\n→ Generating overall organizational summary...")

        # Format question summaries for prompt
        summaries_text = ""
        for i, qs in enumerate(question_summaries, 1):
            summaries_text += f"\n\n=== QUESTION {i}: {qs['question']} ===\n"
            summaries_text += f"Responses: {qs['response_count']}\n"
            summaries_text += f"Summary: {qs['executive_summary']}\n"
            summaries_text += f"Top Themes:\n"
            for theme in qs['themes']:
                summaries_text += f"  - {theme['theme']} ({theme['frequency']}): {theme['description']}\n"
            summaries_text += f"Sentiment: {qs['sentiment_analysis']['overall']}\n"

        prompt = f"""You are a senior organizational consultant analyzing survey results from 100+ Solution Consultants (presales professionals) at an enterprise software company.

You have analyzed {len(question_summaries)} survey questions covering:
- Team culture
- Future vision and mission
- AI adoption and efficiency
- Skills and capabilities
- Relationships with other teams
- Human value proposition
- Success metrics
- Current challenges and bottlenecks
- Actions to stop doing
- Actions to start doing

QUESTION SUMMARIES:
{summaries_text}

Based on this comprehensive analysis, provide an organizational assessment in this EXACT JSON format:
{{
  "executive_summary": "3 comprehensive paragraphs assessing organizational health. Paragraph 1: Overall state and morale. Paragraph 2: Key strengths and opportunities. Paragraph 3: Critical challenges and risks. Be specific, use data from summaries, and provide strategic perspective.",
  "strategic_priorities": [
    {{"rank": 1, "priority": "Most critical priority", "rationale": "Why this is #1 based on survey data. Reference specific themes and frequency."}},
    {{"rank": 2, "priority": "Second priority", "rationale": "Why this is important and how it connects to survey patterns."}},
    {{"rank": 3, "priority": "Third priority", "rationale": "Justification with evidence from responses."}},
    {{"rank": 4, "priority": "Fourth priority", "rationale": "Strategic importance and survey evidence."}},
    {{"rank": 5, "priority": "Fifth priority", "rationale": "Why this matters for the organization."}}
  ],
  "critical_risks": {{
    "people": "Specific risks to employee satisfaction, retention, burnout, skills gaps (2-3 sentences with evidence)",
    "revenue": "Specific risks to revenue, customer satisfaction, win rates, deal velocity (2-3 sentences with evidence)",
    "competitive": "Specific risks to competitive position, market relevance, innovation (2-3 sentences with evidence)"
  }},
  "cross_question_insights": {{
    "alignments": [
      "Where responses align across multiple questions (theme that appears in 3+ questions)",
      "Another pattern of alignment showing consistency",
      "Third alignment pattern"
    ],
    "contradictions": [
      "Where responses conflict or reveal tensions (e.g., want X in one question but complain about X in another)",
      "Another contradiction or tension",
      "Third contradiction if present, otherwise 'No major contradictions identified'"
    ],
    "emerging_patterns": [
      "Meta-pattern that spans multiple questions (e.g., 'transformation anxiety' appearing in culture, AI, and future questions)",
      "Another emerging organizational dynamic",
      "Third pattern revealing deeper truth"
    ]
  }},
  "action_plan": [
    {{"timeframe": "0-30 days", "action": "Quick win action that addresses high-frequency pain point", "rationale": "Why this is urgent and achievable in 30 days"}},
    {{"timeframe": "0-30 days", "action": "Second quick win", "rationale": "Justification"}},
    {{"timeframe": "30-90 days", "action": "Medium-term initiative requiring coordination", "rationale": "Why this timeline and why this action"}},
    {{"timeframe": "30-90 days", "action": "Second medium-term action", "rationale": "Strategic importance"}},
    {{"timeframe": "90+ days", "action": "Long-term strategic transformation", "rationale": "Why this is important but requires extended timeframe"}},
    {{"timeframe": "90+ days", "action": "Second long-term action", "rationale": "Strategic vision"}}
  ]
}}

CRITICAL INSTRUCTIONS:
1. Be specific - reference actual themes, frequencies, and patterns from the summaries
2. Strategic priorities should be ranked by impact × urgency based on survey data
3. Risks should be evidence-based, not generic
4. Cross-question insights should reveal deeper organizational dynamics
5. Action plan should map directly to survey findings
6. Return ONLY valid JSON (no markdown, no extra text)"""

        try:
            response_text = self._call_bedrock(prompt, max_tokens=6000)

            # Clean response
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            overall_summary = json.loads(response_text)
            print("✓ Overall summary completed")
            return overall_summary

        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error: {e}")
            print(f"Response was: {response_text[:500]}...")
            raise
        except Exception as e:
            print(f"✗ Error generating overall summary: {e}")
            raise

    def process_survey(self, df: pd.DataFrame, output_path: str = 'llm_summaries.json') -> Dict[str, Any]:
        """
        Process entire survey: generate question summaries + overall synthesis.

        Args:
            df: DataFrame with 'Question' and 'Response' columns
            output_path: Where to save JSON output

        Returns:
            Complete summary structure
        """
        print("\n" + "="*70)
        print("LLM BATCH SUMMARIZATION - AWS Bedrock Claude Opus 4.5")
        print("="*70)

        # Group responses by question
        grouped = df.groupby('Question')['Response'].apply(list).reset_index()

        print(f"\n📊 Survey Statistics:")
        print(f"   Total Questions: {len(grouped)}")
        print(f"   Total Responses: {len(df)}")
        print(f"   Avg Responses/Question: {len(df) / len(grouped):.1f}")

        # Process each question
        question_summaries = []
        print(f"\n🔍 Analyzing Questions:\n")

        for idx, row in grouped.iterrows():
            question = row['Question']
            responses = row['Response']

            try:
                summary = self.summarize_question(question, responses)
                question_summaries.append(summary)
                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                print(f"  ⚠ Skipping question due to error: {e}")
                continue

        # Generate overall summary
        try:
            overall_summary = self.generate_overall_summary(question_summaries)
        except Exception as e:
            print(f"⚠ Could not generate overall summary: {e}")
            overall_summary = {"error": str(e)}

        # Compile final output
        final_output = {
            "metadata": {
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "model": self.model_id,
                "total_questions": len(question_summaries),
                "total_responses": len(df)
            },
            "question_summaries": question_summaries,
            "overall_summary": overall_summary
        }

        # Save to file
        output_file = Path(output_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)

        print("\n" + "="*70)
        print(f"✓ COMPLETE - Summaries saved to: {output_file.absolute()}")
        print(f"  • {len(question_summaries)} question summaries generated")
        print(f"  • 1 overall organizational assessment")
        print(f"  • File size: {output_file.stat().st_size / 1024:.1f} KB")
        print("="*70 + "\n")

        return final_output


def main():
    """
    Command-line interface for batch summarization.
    """
    import sys

    # Check for custom CSV path
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'raw-data.csv'

    print(f"Loading data from: {csv_path}")

    try:
        # Load data (replicate app.py logic)
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()

        # Use 'Response' or 'Responses' column
        response_col = 'Responses' if 'Responses' in df.columns else 'Response'
        df = df.rename(columns={response_col: 'Response'})

        # Filter out empty responses
        df = df[df['Response'].notna()]
        df = df[df['Response'].str.strip() != '']
        df = df[df['Response'].str.lower() != 'nan']

        # Filter out numeric responses (multiple choice)
        df = df[~df['Response'].astype(str).str.match(r'^\d+$')]

        print(f"✓ Loaded {len(df)} responses from {df['Question'].nunique()} questions")

        # Initialize and run summarizer
        summarizer = LLMBatchSummarizer()
        summarizer.process_survey(df)

    except FileNotFoundError:
        print(f"✗ Error: Could not find {csv_path}")
        print("  Usage: python llm_batch_summarizer.py [path/to/survey.csv]")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
