# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Presales Survey Analysis Toolkit** designed to transform 100+ survey responses from an International Presales All-Hands into strategic intelligence and actionable insights through interactive data visualization and sentiment analysis.

**Core Purpose:** Extract meaningful insights from open-ended survey responses to inform presales team transformation in 2025-2027.

## Repository Structure

### Core Application Files
- **`app.py`** - Streamlit interactive dashboard for data visualization and analysis
- **`raw-data.csv`** - Exported survey responses in Question/Response format from Menti.com
- **`requirements.txt`** - Python dependencies for the web app
- **`venv/`** - Python virtual environment (not in git)

### Documentation
- **`README.md`** - User-facing getting started guide and usage instructions
- **`CLAUDE.md`** - This file - technical documentation for AI assistants
- **`Future plan.md`** - Roadmap and planned enhancements

## Survey Structure

The survey contains 14 questions covering:
1. **Q1** - Team Culture
2. **Q2** - Future Mission (2-year horizon)
3. **Q3-Q5** - Skills and capabilities (includes 2 multiple choice questions)
4. **Q6** - AI desired use cases
5. **Q7** - AI tools currently used
6. **Q11** - Uniquely human value proposition
7. **Q12** - Top operational challenges
8. **Q13** - Stop Doing (pain points to eliminate)
9. **Q14** - Start Doing (new initiatives)

12 questions are open-ended text responses, 2 are multiple choice (embedded in app.py as hardcoded data).

## Dashboard Architecture

### Quick Start
```bash
# Activate virtual environment
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

# Launch dashboard
streamlit run app.py
```

The app opens at `http://localhost:8501` with six analysis views.

### Dashboard Views

**1. Overview (📈)**
- Total response metrics and distribution
- Response counts per question
- Summary statistics table

**2. Multiple Choice Results (🎲)**
- Future Roles: Vote distribution (6 role options, hardcoded in app.py lines 137-147)
- Future Skillsets: Ranking results (5 skillsets, hardcoded in app.py lines 149-159)

**3. Question Deep Dive (❓)**
- Interactive word clouds (matplotlib + WordCloud library)
- Top word frequency analysis
- Bar charts of word distribution (Plotly)
- Random sample responses for qualitative review

**4. Sentiment Analysis (💭)**
- **Question-Aware Sentiment Classification** (context-intelligent, not just lexical)
- Automatic classification into Positive/Neutral/Negative with confidence scores
- Three-column display: Most Positive, Most Neutral, Most Negative responses
- Sentiment distribution pie charts with percentage breakdowns
- 8-rule contextual analysis system (see Sentiment Analysis section below)

**5. Quick Wins Analysis (🎯)**
- Dedicated view for "Stop Doing" and "Start Doing" questions
- Side-by-side word clouds
- Top pain points and initiatives ranked by frequency
- Impact × Effort matrix framework for prioritization

**6. Cross-Question Correlation (📊)**
- Compare any two questions side-by-side
- Identify common themes across questions
- Spot gaps between aspiration vs reality

### Export Capabilities
- Right-click any Plotly chart → "Download plot as PNG"
- Word clouds: Right-click → "Save image as..."
- Use exported charts directly in PowerPoint presentations

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

## Data Format Standards

### CSV Structure
```
Question,Response
[Full question text],[Single response text]
```
- Each row = one response to one question
- Questions are repeated across rows
- Responses can be single words or long-form text
- UTF-8 encoding required

### Data Filtering

The app automatically filters data (app.py lines 98-131):
- Removes empty responses
- Removes "nan" string values
- Separates numeric responses (multiple choice vote counts) from text responses
- Filters questions with <10 responses to reduce noise

## Code Modification Guidelines

### When working with app.py:

**Color Scheme (lines 15-45)**
- Centralized COLOR_SCHEME dictionary
- Google Maps-inspired blue/orange theme
- Update here to change entire app color palette

**Data Loading (lines 98-131)**
- `load_data()` function handles CSV parsing
- Returns two DataFrames: open_ended and multiple_choice
- Modify here to support different CSV formats

**Sentiment Analysis (lines 278-577)**
- Well-tested and validated implementation
- If modifying, thoroughly test edge cases
- Use reasoning output to debug classifications

**Visualization Functions (lines 200-276)**
- `create_wordcloud()` - matplotlib-based word clouds
- `create_frequency_chart()` - Plotly horizontal bar charts
- `create_response_distribution()` - Plotly distribution charts
- Update here to change visualization styles

**Main Dashboard (lines 603-1087)**
- Six views organized as if/elif blocks based on `analysis_mode`
- Each view is self-contained
- Add new views by adding elif block and updating sidebar radio options

### Best Practices

- **Preserve color scheme consistency** - Use COLOR_SCHEME dictionary for all colors
- **Maintain caching** - Keep `@st.cache_data` decorators to ensure performance
- **Test with real data** - Always test modifications against raw-data.csv
- **Update line number references** - If you add/remove code, update line numbers in documentation

## Common Tasks

### Adding a New Dashboard View

1. Add option to sidebar radio (app.py around line 620)
2. Add elif block in main() function
3. Use existing visualization functions or create new ones
4. Follow existing view structure for consistency

### Adding a New Keyword to Sentiment Analysis

1. Locate PAIN_KEYWORDS or STRENGTH_KEYWORDS (app.py ~lines 326-337)
2. Add keyword to list
3. Test on sample data to verify impact
4. Document in comments why keyword was added

### Changing Visualization Colors

1. Update COLOR_SCHEME dictionary (app.py lines 15-45)
2. Changes automatically apply to all charts
3. Test all dashboard views to ensure consistency

### Supporting New Question Types

1. Add question patterns to QUESTION_CONTEXT (app.py ~line 282)
2. Test sentiment analysis on new questions
3. Adjust bias weights if needed

## Key Insights

This is **not academic research** - aim for directionally correct insights, not perfect statistical rigor:
- Focus on actionable intelligence over academic rigor
- Use representative quotes to validate quantitative findings
- Triangulate across multiple questions to build confidence
- Validate themes with stakeholders, not just data

The goal is strategic intelligence that drives organizational transformation, not a peer-reviewed research paper.
