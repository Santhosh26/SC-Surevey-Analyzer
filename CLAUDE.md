# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Presales Survey Analysis Toolkit** designed to transform 100+ survey responses from an International Presales All-Hands into strategic intelligence and actionable insights through interactive data visualization and sentiment analysis.

**Core Purpose:** Extract meaningful insights from open-ended survey responses to inform presales team transformation in 2025-2027.

## Quick Start Commands

**Setup (one-time):**
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download TextBlob corpora (required for sentiment analysis)
python -m textblob.download_corpora
```

**Development:**
```bash
# Run the dashboard
streamlit run app.py

# Access at: http://localhost:8501
# Use --server.port 8502 flag to use different port if needed
```

**Debugging:**
```bash
# View app logs (Streamlit debug output)
streamlit run app.py --logger.level=debug

# Profile sentiment analysis performance
python -c "from app import load_data; import time; start = time.time(); load_data(); print(f'Load time: {(time.time()-start)*1000:.2f}ms')"
```

**LLM Features (Optional - requires AWS Bedrock setup):**
```bash
# Generate AI-powered summaries using Claude Opus 4.5
python llm_batch_summarizer.py

# Validate LLM outputs for hallucinations
python llm_eval_validator.py

# View AI insights in dashboard
streamlit run app.py  # Then go to "🤖 AI Insights" tab
```

## Repository Structure

- **`app.py`** - Streamlit interactive dashboard (1,267 lines) - see Architecture section
- **`llm_batch_summarizer.py`** - AWS Bedrock integration for batch LLM summaries (19KB)
- **`llm_eval_validator.py`** - Validation suite for LLM outputs (29KB)
- **`raw-data.csv`** - Survey responses in "Question,Response" format from Menti.com
- **`requirements.txt`** - Python dependencies (12 packages, pinned versions)
- **`.streamlit/`** - Streamlit configuration directory
- **`.claude/settings.local.json`** - Claude Code permissions (allows Python execution)
- **Documentation:** README.md (user guide), CLAUDE.md (technical docs), AWS_BEDROCK_SETUP.md (LLM setup), Future plan.md (roadmap)

## Application Architecture

### Core Abstractions

**`app.py` is organized into 4 main sections:**

1. **Configuration (lines 1-95)** - Color scheme, page setup, CSS styling
2. **Data Processing (lines 98-277)** - Load, clean, tokenize survey responses
3. **Sentiment Analysis Engine (lines 278-577)** - Question-aware contextual classification
4. **UI & Dashboard (lines 603-1267)** - Seven interactive views with caching

### Key Functions

**Data Pipeline:**
- `load_data()` - Parses CSV, filters questions (<10 responses excluded), splits open-ended vs multiple choice
- `tokenize_responses()` - Removes stopwords, lemmatizes, caches results

**Sentiment Engine:**
- `new_contextual_sentiment(response, question_text, question_context)` - Returns (sentiment, confidence, reasoning)
- Implements 8-rule scoring system with question bias awareness and gap detection

**Visualization:**
- `create_wordcloud()` - matplotlib-based word clouds with plasma colormap
- `create_frequency_chart()` - Plotly horizontal bar charts with interactive filtering
- `create_response_distribution()` - Sentiment breakdowns and sample responses

### Survey Data (14 questions)

Open-ended questions: Q1 (culture), Q2 (mission), Q6-Q7 (AI), Q11 (human value), Q12 (challenges), Q13-Q14 (stop/start)
Multiple choice questions: Q3-Q4 (hardcoded in app.py lines 137-159) - Future Roles & Skillsets

## Dashboard Views (7 Interactive Tabs)

All views use `@st.cache_data` for performance. Views are implemented as if/elif blocks in `main()` (app.py ~line 622).

| View | Purpose | Key Features |
|------|---------|--------------|
| **📈 Overview** | Survey health check | Total responses, distribution per question, summary stats |
| **🎲 Multiple Choice** | Vote distribution (Q3-Q4) | Future Roles (6 options), Skillsets ranking (5 options) |
| **❓ Deep Dive** | Question-level analysis | Word clouds, top N word frequency, sample responses |
| **💭 Sentiment** | Opinion extraction | Positive/Neutral/Negative with confidence, per-question sentiment distribution |
| **🤖 AI Insights** | LLM-powered analysis | AWS Bedrock batch summaries, hallucination detection, strategic recommendations |
| **🎯 Quick Wins** | Action prioritization | Stop Doing + Start Doing analysis, frequency ranking, Impact×Effort framework |
| **📊 Correlation** | Cross-question patterns | Side-by-side comparison of any two questions |

**Exports:**
- Plotly charts: Right-click → "Download plot as PNG"
- Word clouds: Right-click → "Save image as..."

## Sentiment Analysis Implementation

### Overview

The dashboard uses a **Question-Aware Sentiment Analysis System** (app.py lines 278-577) that goes beyond simple lexical polarity (TextBlob baseline) to understand the **survey context** of each response.

**Key Insight:** Grammatically positive words can indicate negative situations in surveys.

**Example:** "More collaboration" contains the positive word "collaboration", but in a survey context, "more X" indicates we **lack** X - this is a gap, not praise.

### Architecture

**Location:** `app.py` lines 278-577 (configuration and functions), lines 862-943 (UI)

**Core Function:** `new_contextual_sentiment(response, question_text, question_context)` → `(sentiment, confidence, reasoning)`

**Components:**
1. **Question Context Detection** - Identifies if question has negative_bias, positive_bias, or neutral context
2. **Gap Indicator Detection** - Finds "more X", "better X", "need X" patterns (12 patterns)
3. **Negation Detection** - Context-aware detection of "not", "stop", "can't" (7 patterns)
4. **Keyword Matching** - Pain keywords (~25) and Strength keywords (~18)
5. **TextBlob Override Dictionary** - Fixes known lexical quirks ("base", "knowledge base", "poc")
6. **8-Rule Scoring System** - Combines all signals with weighted adjustments
7. **Confidence Calculation** - 0.0-1.0 score based on number of signals detected
8. **Reasoning Generation** - Explains classification for transparency

### Question Context Categories

```python
QUESTION_CONTEXT = {
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
```

**Purpose:** Questions have inherent bias. "STOP doing" responses are complaints (negative context), while "START doing" responses are suggestions (positive context).

### Eight-Rule Scoring System

**Base Score:** TextBlob polarity (-1.0 to +1.0)

**Rule 1: Question Context Bias**
- Negative-bias questions: -0.4 adjustment
- Positive-bias questions: +0.5 adjustment
- Neutral questions: no adjustment

**Rule 2: Gap Indicators** (-0.5 penalty)
- Patterns: "more X", "better X", "need X", "lack of", "without", "missing", "improve X"
- **Priority:** Overrides strength keywords (gaps take precedence)
- Example: "More collaboration" → Neutral (gap detected, strength bonus skipped)

**Rule 3: Negation Patterns** (-0.4 penalty)
- Patterns: "not", "no X", "can't", "cannot", "won't", "stop", "never"
- **Context-aware:** "stop" in START DOING questions is constructive, not negative
- Example: "Stop spoon feeding AE" in START DOING → Positive (negation skipped)

**Rule 4: Pain Keywords** (-0.3 penalty)
- Keywords: challenge, difficult, stress, overwork, frustration, gap, bottleneck, confusion
- ~25 keywords covering operational pain points

**Rule 5: Strength Keywords** (+0.3 bonus, IF no gap indicator)
- Keywords: trust, empathy, innovation, collaboration, expertise, quality, commitment
- ~18 keywords covering team strengths
- **Conditional:** Only applied if gap indicator is NOT present

**Rule 6: Short Response Context** (±0.2 adjustment)
- If response ≤ 3 words:
  - Negative-bias questions: -0.2 (likely pain point)
  - Positive-bias questions: +0.2 (likely strength)
  - Reduces confidence by -0.1 (less signal)

**Rule 7: POC Edge Case** (-0.4 penalty)
- "POC" in negative-bias questions (STOP DOING) → strong negative signal
- POC (Proof of Concept) is a known pain point in presales

**Rule 8: Listening Gap Edge Case** (-0.5 penalty)
- Special handling for "listen more", "active listening"
- High confidence (+0.25)
- Example: "Listen more" → Negative (gap), "Active listening" → Negative (gap)

### Uncertainty Detection (Special Case)

**Rule 2.5:** Uncertainty patterns force Neutral classification
- Patterns: "not sure", "unsure", "don't know", "uncertain"
- Overrides all other rules to prevent misclassification
- Example: "I'm not sure" → Neutral (not negative despite "not")

### Final Classification Thresholds

```python
if sentiment_score > 0.1:
    sentiment = 'Positive'
elif sentiment_score < -0.1:
    sentiment = 'Negative'
else:
    sentiment = 'Neutral'
```

**Neutral zone:** -0.1 to +0.1 (captures ambiguous responses)

### TextBlob Override Dictionary

**Purpose:** Fix known lexical quirks where TextBlob assigns incorrect polarity

```python
TEXTBLOB_OVERRIDES = {
    'knowledge base': 0.1,      # TextBlob incorrectly gives -0.8 due to "base"
    'base': 0.0,                # TextBlob associates with "base instincts" (negative)
    'poc': 0.0,                 # TextBlob may confuse with "pox" (disease)
    'having a knowledge base': 0.2,  # Explicitly positive in presales context
}
```

**Why needed:** TextBlob is trained on general text, not domain-specific surveys. "Base" in "knowledge base" is neutral/positive in presales, but TextBlob assigns -0.8 polarity.

### Confidence Scoring

**Base confidence:** 0.5-0.7 depending on context detection

**Increases confidence (+0.1 to +0.25) when:**
- Question context detected
- Gap indicator found
- Negation detected
- Pain/strength keywords matched
- Special edge cases triggered (POC, listening)

**Decreases confidence (-0.1) when:**
- Response is very short (≤ 3 words)

**Capped at:** 1.0 maximum

**Interpretation:**
- 0.9-1.0: Very high confidence (multiple strong signals)
- 0.7-0.9: High confidence (typical for most responses)
- 0.5-0.7: Medium confidence (few signals, short response)
- <0.5: Low confidence (ambiguous, needs review)

### Performance

- **Average processing time:** ~0.09ms per response
- **Full dataset (1,434 responses):** ~127ms (0.13 seconds)
- **Overhead vs TextBlob baseline:** <0.01ms (negligible)
- **Caching:** Streamlit `@st.cache_data` decorator ensures analysis runs once per session

### Known Limitations

1. **No sarcasm detection:** "Great, another POC" would be classified as positive
2. **No multi-response context:** Each response analyzed independently
3. **Language:** English only (TextBlob limitation)
4. **Domain-specific:** Optimized for presales surveys, may need adjustment for other contexts
5. **Compound sentiments:** "Good team but overworked" classified by strongest signal

These limitations are inherent to rule-based systems. Addressing them would require ML/LLM approaches (e.g., fine-tuned transformer models or GPT-4 API integration).

## Modifying Sentiment Analysis

### When to Modify

**Add new keywords** when you notice frequent misclassifications:
- Edit `PAIN_KEYWORDS` (app.py around line 326) for negative indicators
- Edit `STRENGTH_KEYWORDS` (app.py around line 333) for positive indicators

**Add new gap patterns** when you see new linguistic patterns indicating needs:
- Edit `GAP_PATTERNS` (app.py around line 298) with new regex patterns

**Add TextBlob overrides** when specific words/phrases have wrong polarity:
- Edit `TEXTBLOB_OVERRIDES` (app.py around line 436) with domain-specific corrections

**Adjust scoring weights** if overall classification seems too positive/negative:
- Modify adjustment values in `new_contextual_sentiment()` (app.py around lines 414-556)
- Current values: question_bias (±0.4-0.5), gaps (-0.5), negation (-0.4), keywords (±0.3), short responses (±0.2)

**Add new question contexts** when analyzing new survey questions:
- Edit `QUESTION_CONTEXT` (app.py around line 282) to categorize new questions

### Best Practices

1. **Always review low-confidence classifications** - Filter by confidence < 0.7 for manual review
2. **Use sentiment as directional signal, not absolute truth** - Cross-reference with word clouds
3. **Update keywords quarterly** - Survey language evolves; add new terms as they emerge
4. **Compare sentiment across questions** - Look for patterns (e.g., high negative in STOP DOING, high positive in team culture)
5. **Export reasoning for validation** - Reasoning strings explain WHY classification was chosen
6. **Don't over-interpret neutral responses** - Neutral often means "unclear" or "mixed", not "mediocre"

## Analysis Methodology

### Cross-Question Analysis Patterns

Critical insight combinations:
- **Vision vs Reality:** Q2 (future mission) + Q12 (current challenges)
- **Capability Gap:** Q6 (AI desired use) + Q7 (AI current use)
- **Value Delivery:** Q11 (human strengths) + Q12 (constraints)
- **Action Planning:** Q13 (stop doing) + Q14 (start doing) + Q5 (skills needed)

### Quick Wins Prioritization Framework

Use 2×2 matrix (Impact × Effort):
- **P1 (High Impact, Low Effort):** Launch within 0-30 days
- **P2 (High Impact, High Effort):** Medium-term roadmap (30-90 days)
- **P3 (Low Impact, Low Effort):** Quick wins but lower priority
- **P4 (Low Impact, High Effort):** Deprioritize or eliminate

Frequency threshold for prioritization:
- **High frequency:** >30% of respondents
- **Medium frequency:** 15-30% of respondents
- **Low frequency:** <15% of respondents

## Data Format & Processing

### CSV Input Format
```
Question,Response
"How would you describe our team culture?","Collaborative and innovative"
"What is our future mission?","Trusted advisor to customers"
```

**Requirements:**
- Header: `Question,Response` or `Question,Responses`
- Encoding: UTF-8
- Format: Each row = one response to one question (questions repeated)
- The app auto-filters: empty responses, "nan" strings, questions with <10 responses

### Data Filtering (app.py lines 98-131)
- `load_data()` separates open_ended (text) from multiple_choice (numeric) DataFrames
- Multiple choice: hardcoded Q3-Q4 vote arrays + parsed numeric responses
- Open-ended: deduplicated questions, sorted by response count
- Only questions ≥10 responses included (reduces noise)

## Development Workflow

### Making Changes to app.py

**1. Identify the section:**
- Configuration: lines 1-95 (COLOR_SCHEME, page config, CSS)
- Data Processing: lines 98-277 (load_data, tokenization, helpers)
- Sentiment Engine: lines 278-577 (QUESTION_CONTEXT, gap patterns, scoring)
- Dashboard UI: lines 603-1087 (main view logic, if/elif blocks)

**2. Test changes:**
```bash
# Quick test specific function
python -c "from app import load_data, tokenize_responses; load_data()"

# Run full app and inspect output
streamlit run app.py
```

**3. Validate sentiment changes:**
- Always test edge cases (gap indicators, negations, domain keywords)
- Use reasoning output to debug: check why a response was classified
- Compare against word clouds to validate directional accuracy

**4. Preserve performance:**
- Keep `@st.cache_data` decorators on expensive functions
- Don't remove caching or you'll tank performance (sentiment ~0.13s on 1,434 responses)

### Common Modifications

| Task | Location | Notes |
|------|----------|-------|
| Change colors globally | COLOR_SCHEME dict (lines 17-45) | All charts use this automatically |
| Add sentiment keyword | PAIN_KEYWORDS or STRENGTH_KEYWORDS (~line 326) | Test impact on 5-10 sample responses |
| Add gap pattern | GAP_PATTERNS (~line 298) | Use regex; gaps override strength keywords |
| Add question context | QUESTION_CONTEXT (~line 282) | Categorize as negative_bias/positive_bias/neutral |
| Add dashboard view | main() if/elif (~line 622) | Copy existing view structure; add sidebar option |
| Support new CSV format | load_data() (~line 99) | Test with sample CSV; maintain open_ended/multiple_choice split |

## Debugging & Troubleshooting

### Common Issues

**"No module named streamlit"**
- Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
- Reinstall: `pip install -r requirements.txt`

**"TextBlob download error"**
- Run: `python -m textblob.download_corpora`
- This downloads required corpora for sentiment analysis

**"Port 8501 already in use"**
- Use: `streamlit run app.py --server.port 8502` (or any free port)

**Sentiment analysis seems off**
- Check confidence scores (<0.7 = lower confidence, needs review)
- Compare against word clouds (word frequency should align with sentiment)
- Use "Sentiment breakdown by question" to see patterns across similar questions

### Testing Sentiment Classifications

**Quick test specific responses:**
```python
from app import new_contextual_sentiment, QUESTION_CONTEXT

response = "More collaboration needed"
question = "What should we START doing differently tomorrow?"
sentiment, confidence, reasoning = new_contextual_sentiment(response, question, QUESTION_CONTEXT)
print(f"{response} → {sentiment} (confidence: {confidence:.2f})")
print(f"Reasoning: {reasoning}")
```

**Find misclassified responses:**
1. Go to Sentiment Analysis view
2. Filter by low confidence (<0.6)
3. Review reasoning string to understand why it was classified
4. If pattern emerges: add keyword to PAIN_KEYWORDS/STRENGTH_KEYWORDS or update gap patterns

### Performance Profiling

**Full data load time:**
```bash
python -c "from app import load_data; import time; start=time.time(); load_data(); print(f'{(time.time()-start)*1000:.2f}ms')"
```

**Expected baseline:** ~130ms (with caching) for 1,434 responses across 14 questions

## LLM Features (AWS Bedrock Integration)

### Overview

The dashboard includes two LLM-powered scripts that use AWS Bedrock to generate AI insights:

1. **`llm_batch_summarizer.py`** - Generates strategic summaries for each question and overall insights using Claude Opus 4.5
2. **`llm_eval_validator.py`** - Validates LLM outputs to detect hallucinations and inconsistencies

### Setup Requirements (Optional)

LLM features are **optional** - the dashboard works without AWS configuration. To enable:

1. **Set up AWS Bedrock credentials:**
   - Follow the complete guide in `AWS_BEDROCK_SETUP.md`
   - Choose between API Key method (recommended) or traditional AWS credentials
   - Estimated cost: ~$2-3 per full run, or ~$8/month for weekly regeneration

2. **Configure environment:**
   ```bash
   # Copy the example env file
   copy .env.example .env

   # Add your AWS Bedrock API Key to .env
   AWS_BEARER_TOKEN_BEDROCK=your_actual_api_key_here
   ```

### Running LLM Scripts

**Generate batch summaries (requires AWS setup):**
```bash
python llm_batch_summarizer.py
```

Output:
- Generates Claude Opus 4.5 summaries for each question (Q1-Q14)
- Creates overall strategic insights and recommendations
- Saves results to `llm_summaries.json`
- Processing time: ~2-5 minutes depending on dataset size
- Cost: ~$2-3 per run

**Validate LLM outputs:**
```bash
python llm_eval_validator.py
```

Output:
- Detects hallucinations in generated summaries
- Reports consistency scores (0.0-1.0)
- Flags suspicious patterns or unsupported claims
- Saves validation results to `validation_report.json`

**View AI Insights in dashboard:**
1. Run `streamlit run app.py`
2. Navigate to "🤖 AI Insights" tab
3. Click "🚀 Generate AI Summaries" (requires AWS configured)
4. Review summaries alongside frequency data and sentiment analysis

### Architecture

**llm_batch_summarizer.py:**
- Loads survey data and groups by question
- Sends each question's responses to Claude Opus 4.5 via AWS Bedrock
- Builds strategic recommendations from individual summaries
- Implements retry logic and rate limiting
- Saves structured JSON output with timestamps

**llm_eval_validator.py:**
- Compares LLM outputs against source data
- Detects factual inconsistencies
- Uses fuzzy string matching for semantic similarity
- Flags patterns like:
  - Numbers/statistics mentioned in summary not in source
  - Contradictions with survey data
  - Over-generalization from limited responses

### Cost Management

- **Budget tracking:** Set up AWS Budgets with email alerts (see AWS_BEDROCK_SETUP.md)
- **Cost monitoring:** Check AWS Cost Explorer filtered by Bedrock service
- **Optimization:**
  - Generate summaries monthly instead of weekly
  - Use Haiku model for less critical summaries (10x cheaper)
  - Cache results to avoid regenerating unchanged data

### Troubleshooting LLM Features

**"AWS_BEARER_TOKEN_BEDROCK not found"**
- Ensure `.env` file exists and contains the API key
- Run: `echo $AWS_BEARER_TOKEN_BEDROCK` to verify environment variable is set
- On Windows: Use `set AWS_BEARER_TOKEN_BEDROCK=...` if not using .env

**"ValidationException: The provided model identifier is invalid"**
- Model access not enabled in AWS Bedrock console
- See AWS_BEDROCK_SETUP.md Step 1.2 for enabling model access
- Try waiting 5 minutes for permissions to propagate

**"ThrottlingException: Rate exceeded"**
- AWS Bedrock has rate limits (~100 requests/min for Opus)
- The batch summarizer includes delays between requests
- Wait a few minutes and retry

**LLM outputs seem hallucinated**
- Run `llm_eval_validator.py` to detect inconsistencies
- Review reasoning from sentiment analysis for ground truth
- Lower-confidence sentiment classifications may signal unreliable source data

### When to Use LLM Features

- **Use:** Need strategic narrative alongside quantitative analysis
- **Don't use:** Budget constraints or AWS setup complexity
- **Combine with:** Always triangulate LLM insights with word clouds, sentiment scores, and direct quotes from responses

## Key Insights

This is **not academic research** - aim for directionally correct insights, not perfect statistical rigor:
- Focus on actionable intelligence over academic rigor
- Use representative quotes to validate quantitative findings
- Triangulate across multiple questions to build confidence
- Validate themes with stakeholders, not just data

The goal is strategic intelligence that drives organizational transformation, not a peer-reviewed research paper.
