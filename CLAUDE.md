# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Presales Survey Analysis Toolkit** designed to transform 100+ survey responses from an International Presales All-Hands into strategic intelligence and actionable insights. The toolkit provides a structured methodology for thematic coding, analysis, and reporting.

**Core Purpose:** Extract meaningful insights from open-ended survey responses to inform presales team transformation in 2025-2027.

## Repository Structure

### Core Data Files
- **`raw-data.csv`** - Exported survey responses in Question/Responses format from Menti.com
- **`presales_survey_analysis.xlsx`** - Primary analysis workbench with 17 interconnected worksheets (Dashboard, RawData, Q1-Q14 analysis sheets, Theme_Codes, Q4_Rankings, Quick_Wins, Executive_Summary, AI_Analysis_Helper, Sample_Data_Format)

### Methodology Frameworks (Markdown)
- **`README_START_HERE.md`** - Complete project roadmap with 4-week timeline, getting started guide, and success criteria
- **`Thematic_Coding_Framework.md`** - 8-phase systematic analysis methodology for open-ended responses
- **`Quick_Wins_Guide.md`** - 7-phase extraction process for immediate action items (0-30 days)
- **`Executive_Summary_Template.md`** - Structured reporting template for leadership presentation
- **`README_WEB_APP.md`** - Web app setup and usage guide

### Web Application
- **`app.py`** - Streamlit interactive dashboard for data visualization and analysis
- **`requirements.txt`** - Python dependencies for the web app
- **`run_app.bat`** - Windows batch script to launch the dashboard
- **`venv/`** - Python virtual environment (not in git)

### Validation and Testing
- **`VALIDATION_SUMMARY.md`** - Executive summary of sentiment analysis validation
- **`IMPLEMENTATION_REVIEW_REPORT.md`** - Detailed technical review of sentiment analysis
- **`REVIEW_EXECUTIVE_SUMMARY.md`** - Deployment readiness assessment
- **`validate_latest_fixes.py`** - Comprehensive test suite for sentiment analysis (10 test cases)
- **`search_real_data.py`** - Real data validation script for user-reported issues
- **`validation_test_results.csv`** - Test results export
- **`comprehensive_review_test.py`** - Initial implementation testing suite
- **`verify_fix.py`** - Bug fix verification script

## Survey Question Structure

The survey contains 14 questions covering:
1. **Q1** - Team Culture
2. **Q2** - Future Mission (2-year horizon)
3. **Q3-Q5** - Skills and capabilities
4. **Q6** - AI desired use cases
5. **Q7** - AI tools currently used
6. **Q11** - Uniquely human value proposition
7. **Q12** - Top operational challenges
8. **Q13** - Stop Doing (pain points to eliminate)
9. **Q14** - Start Doing (new initiatives)

## Analysis Workflow

### Phase 1: Data Import & Coding (Week 1)
1. Export Menti.com data to Excel/CSV
2. Import into `RawData` sheet in the workbook
3. Add Response IDs (R001, R002, etc.)
4. Develop theme codes (5-7 per question) using the framework
5. Code all responses using thematic analysis

### Phase 2: Synthesis & Cross-Analysis (Week 2)
1. Calculate theme frequencies
2. Extract representative quotes (2-3 per theme)
3. Perform cross-question analysis to identify patterns:
   - Q2 (Mission) vs Q12 (Challenges) = vision vs reality gap
   - Q6 (AI want) vs Q7 (AI use) = capability gap
   - Q11 (Human value) vs Q12 (Challenges) = delivery constraints
4. Identify strategic tensions and trade-offs

### Phase 3: Quick Wins Extraction (Week 3)
1. Extract all Stop/Start items from Q13/Q14
2. Group by semantic similarity
3. Calculate frequency
4. Assess Impact × Effort using 2×2 matrix
5. Select top 3-5 P1 quick wins
6. Create detailed action plans with owners and timelines

### Phase 4: Reporting (Week 4)
1. Complete Executive Summary template
2. Create presentation slides (15-20 slides)
3. Launch first quick wins
4. Present to leadership

## Web App - Interactive Dashboard

### Quick Start
```bash
# Windows
run_app.bat

# Or manually
venv\Scripts\activate
streamlit run app.py
```

The app opens at `http://localhost:8501` with five analysis views:

### Dashboard Features

**1. Overview (📈)**
- Total response metrics and distribution
- Response counts per question
- Summary statistics table

**2. Question Deep Dive (❓)**
- Interactive word clouds
- Top word frequency analysis
- Bar charts of word distribution
- Random sample responses for qualitative review

**3. Sentiment Analysis (💭)**
- **Question-Aware Sentiment Classification** (context-intelligent, not just lexical)
- Automatic classification into Positive/Neutral/Negative with confidence scores
- Three-column display: Most Positive, Most Neutral, Most Negative responses
- Sentiment distribution pie charts with percentage breakdowns
- Understands survey context (e.g., "more collaboration" = gap/need, not positive)
- Handles edge cases: listening gaps, constructive "stop" suggestions, POC context
- 8-rule contextual analysis system (see Sentiment Analysis Implementation section)

**4. Quick Wins Analysis (🎯)**
- Dedicated view for "Stop Doing" and "Start Doing" questions
- Side-by-side word clouds
- Top pain points and initiatives ranked by frequency
- Impact × Effort matrix framework for prioritization

**5. Cross-Question Correlation (📊)**
- Compare any two questions side-by-side
- Identify common themes across questions
- Spot gaps between aspiration vs reality

### Export Capabilities
- Right-click any Plotly chart → "Download plot as PNG"
- Word clouds: Right-click → "Save image as..."
- Use exported charts directly in PowerPoint presentations

### Deployment Options
- **Local:** Run during presentation (recommended for quick delivery)
- **Streamlit Cloud:** Free public hosting at share.streamlit.io
- **Docker:** Internal hosting (see README_WEB_APP.md)

### When to Use Web App vs Excel
- **Web App:** Fast exploration, generating charts for presentations, sentiment analysis, cross-question comparisons
- **Excel:** Manual thematic coding, detailed frequency calculations, storing coded responses, formula-based analysis

The web app complements the Excel workbook - use the app for visualization and the workbook for coding.

## Sentiment Analysis Implementation

### Overview

The dashboard uses a **Question-Aware Sentiment Analysis System** that goes beyond simple lexical polarity (TextBlob baseline) to understand the **survey context** of each response. This addresses a critical limitation: grammatically positive words can indicate negative situations in surveys.

**Example:** "More collaboration" contains the positive word "collaboration", but in a survey context, "more X" indicates we **lack** X - this is a gap, not praise.

### Architecture

**Location:** `app.py` lines 278-574 (configuration and functions), lines 858-985 (UI)

**Core Function:** `new_contextual_sentiment(response, question)` → `(sentiment, confidence, reasoning)`

**Components:**
1. **Question Context Detection** - Identifies if question has negative_bias, positive_bias, or neutral context
2. **Gap Indicator Detection** - Finds "more X", "better X", "need X" patterns (12 patterns)
3. **Negation Detection** - Context-aware detection of "not", "stop", "can't" (7 patterns)
4. **Keyword Matching** - Pain keywords (25) and Strength keywords (18)
5. **TextBlob Override Dictionary** - Fixes known lexical quirks ("base", "knowledge base", "poc")
6. **8-Rule Scoring System** - Combines all signals with weighted adjustments
7. **Confidence Calculation** - 0.0-1.0 score based on number of signals detected
8. **Reasoning Generation** - Explains classification for transparency

### Question Context Categories

```python
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
```

**Purpose:** Questions have inherent bias. "STOP doing" responses are complaints (negative context), while "START doing" responses are suggestions (positive context).

### Eight-Rule Scoring System

**Base Score:** TextBlob polarity (-1.0 to +1.0)

**Rule 1: Question Context Bias**
- Negative-bias questions: -0.3 adjustment
- Positive-bias questions: +0.5 adjustment (increased from +0.3 to overcome TextBlob quirks)
- Neutral questions: no adjustment

**Rule 2: Gap Indicators** (-0.5 penalty)
- Patterns: "more X", "better X", "need X", "lack of", "without", "missing", "listening"
- **Priority:** Overrides strength keywords (gaps take precedence)
- Example: "More collaboration" → Neutral (gap detected, strength bonus skipped)

**Rule 3: Negation Patterns** (-0.4 penalty)
- Patterns: "not", "no X", "can't", "cannot", "won't", "stop", "never"
- **Context-aware:** "stop" in START DOING questions is constructive, not negative
- Example: "Stop spoon feeding AE" in START DOING → Positive (negation skipped)

**Rule 4: Pain Keywords** (-0.3 penalty)
- Keywords: challenge, difficult, stress, overwork, frustration, gap, bottleneck, confusion
- 25 total keywords covering operational pain points

**Rule 5: Strength Keywords** (+0.3 bonus, IF no gap indicator)
- Keywords: trust, empathy, innovation, collaboration, expertise, quality, commitment
- 18 total keywords covering team strengths
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
- High confidence (+0.25) due to specific user-reported issue
- Example: "Listen more" → Negative (gap), "Active listening" → Negative (gap)

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

**Base confidence:** 0.7

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

### User-Reported Issues Fixed

The current implementation addresses three specific misclassifications identified during testing:

**Issue 1: "Having_a_knowledge_base" in START DOING**
- **Problem:** Classified as Negative due to TextBlob's -0.8 polarity for "base"
- **Fix:** TextBlob override dictionary assigns 0.2 polarity
- **Result:** Now correctly classified as Positive (confidence: 0.90)

**Issue 2: "Stop_spoon_feeding_ae" in START DOING**
- **Problem:** Classified as Negative due to "stop" negation pattern
- **Fix:** Context-aware negation skips penalty when "stop" appears in positive_bias questions
- **Result:** Now correctly classified as Positive (confidence: 0.80)

**Issue 3: "More collaboration" in PM relationship question**
- **Problem:** Classified as Positive due to "collaboration" strength keyword
- **Fix:** Gap indicators take priority over strength keywords (line 495)
- **Result:** Now correctly classified as Neutral (confidence: 0.80)

### Validation and Testing

**Test Suite:** `validate_latest_fixes.py` (10 comprehensive test cases)
**Real Data Validation:** `search_real_data.py` (tested against 1,434 actual responses)
**Success Rate:** 80% (8/10 tests passed, all user-reported issues resolved)

**Validation Reports:**
- `VALIDATION_SUMMARY.md` - Executive summary of testing results
- `validation_test_results.csv` - Detailed test case results
- `IMPLEMENTATION_REVIEW_REPORT.md` - Technical implementation review
- `REVIEW_EXECUTIVE_SUMMARY.md` - Deployment readiness assessment

### When to Modify Sentiment Analysis

**Add new keywords** when you notice frequent misclassifications:
- Edit `PAIN_KEYWORDS` (line 420) for negative indicators
- Edit `STRENGTH_KEYWORDS` (line 425) for positive indicators

**Add new gap patterns** when you see new linguistic patterns indicating needs:
- Edit `GAP_PATTERNS` (line 340) with new regex patterns

**Add TextBlob overrides** when specific words/phrases have wrong polarity:
- Edit `TEXTBLOB_OVERRIDES` (line 436) with domain-specific corrections

**Adjust scoring weights** if overall classification seems too positive/negative:
- Modify adjustment values in `new_contextual_sentiment()` (lines 455-519)
- Current values: question_bias (±0.3-0.5), gaps (-0.5), negation (-0.4), keywords (±0.3), short responses (±0.2)

**Add new question contexts** when analyzing new survey questions:
- Edit `QUESTION_CONTEXTS` (line 279) to categorize new questions

### Performance

- **Average processing time:** 0.09ms per response
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

### Best Practices for Sentiment Analysis

1. **Always review low-confidence classifications** - Filter by confidence < 0.7 for manual review
2. **Use sentiment as directional signal, not absolute truth** - Cross-reference with thematic coding
3. **Update keywords quarterly** - Survey language evolves; add new terms as they emerge
4. **Compare sentiment across questions** - Look for patterns (e.g., high negative in STOP DOING, high positive in team culture)
5. **Export reasoning for validation** - Reasoning strings explain WHY classification was chosen
6. **Don't over-interpret neutral responses** - Neutral often means "unclear" or "mixed", not "mediocre"

### Integration with Other Analyses

**Sentiment Analysis works best when combined with:**
- **Word Clouds:** Sentiment provides emotional tone, word clouds provide content themes
- **Thematic Coding:** Sentiment is quantitative, themes are qualitative - use both
- **Cross-Question Correlation:** Sentiment comparison reveals emotional gaps (e.g., positive mission vision + negative current reality = frustration)
- **Quick Wins Analysis:** Negative sentiment in STOP DOING highlights urgent pain points

## Key Methodological Principles

### Thematic Coding Best Practices
- **Themes must be mutually exclusive** - minimal overlap between codes
- **Themes must be exhaustive** - cover 90%+ of responses
- **Use 5-7 themes per question** - more leads to analysis paralysis
- **Apply 80/20 rule** - 20% of themes will drive 80% of insights
- **Prioritize triangulation** - look for stories across questions, not just within them

### AI Acceleration Strategy
Use AI (ChatGPT/Claude) to:
- Generate initial theme codes from sample responses (30-40 samples)
- Validate coding schemes
- Extract representative quotes
- NOT as a replacement for human judgment - always validate AI suggestions

### Cross-Question Analysis Patterns
Critical insight combinations:
- **Vision vs Reality:** Q2 (future mission) + Q12 (current challenges)
- **Capability Gap:** Q6 (AI desired use) + Q7 (AI current use)
- **Value Delivery:** Q11 (human strengths) + Q12 (constraints)
- **Action Planning:** Q13 (stop doing) + Q14 (start doing) + Q5 (skills needed)

## Data Format Standards

### CSV Structure
```
Question,Responses
[Full question text],[Single response text]
```
- Each row = one response to one question
- Questions are repeated across rows
- Responses can be single words or long-form text

### Excel Workbook Expectations
- **RawData sheet:** Import template with standardized headers
- **Response IDs:** R001, R002, etc. format
- **Theme Codes:** 4-6 letter abbreviations (e.g., COLLAB, TRUST, INNOV)
- **Color coding:** Built-in for navigation and status tracking
- **Formula validation:** All formulas pre-validated (zero errors)

## Analysis Time Estimates

**Total: 16-20 hours manual | 8-10 hours with AI assistance**

- Week 1 (Data Import & Coding): 8-10 hours
- Week 2 (Analysis & Synthesis): 6-8 hours
- Week 3 (Quick Wins): 4-6 hours
- Week 4 (Reporting): 4-6 hours

## Common Pitfalls to Avoid

1. **DON'T code before reading 30-50 responses** - risk missing important themes
2. **DON'T create 15+ themes per question** - causes analysis paralysis; merge similar themes
3. **DON'T just report data without insights** - every finding needs "So What?" and "Now What?"
4. **DON'T ignore contradictions** - strategic tensions often reveal key decisions needed
5. **DON'T over-promise on quick wins** - under-promise, over-deliver
6. **DON'T forget to close the loop** - always attribute actions back to team feedback

## Quick Wins Prioritization Framework

Use 2×2 matrix (Impact × Effort):
- **P1 (High Impact, Low Effort):** Launch within 0-30 days
- **P2 (High Impact, High Effort):** Medium-term roadmap (30-90 days)
- **P3 (Low Impact, Low Effort):** Quick wins but lower priority
- **P4 (Low Impact, High Effort):** Deprioritize or eliminate

Frequency threshold for prioritization:
- **High frequency:** >30% of respondents
- **Medium frequency:** 15-30% of respondents
- **Low frequency:** <15% of respondents

## Success Metrics

### 30-Day Success
- Analysis complete with documented insights
- 3-5 quick wins identified and actioned
- Executive summary presented to leadership
- Team knows what's changing based on their input

### 90-Day Success
- Quick wins showing measurable impact
- Medium-term initiatives launched
- Team engagement improving
- Leadership funding transformation roadmap

### 12-Month Success
- Presales operating model evolved
- Skills gaps addressed systematically
- Win rates increasing
- Team turnover decreasing

## File Modification Guidelines

When working with this repository:
- **Excel workbook** - The primary analytical tool; preserve all formula integrity
- **Markdown frameworks** - Methodology guides; enhance with examples but don't remove core structure
- **raw-data.csv** - Raw survey export; never modify directly, always work from copies
- **README_START_HERE.md** - Master roadmap; this is the entry point for new analysts
- **app.py sentiment analysis (lines 278-574)** - Extensively tested and validated; if modifying, run `validate_latest_fixes.py` to verify no regressions
- **Validation scripts** - Reference implementations for testing; preserve for future regression testing

## Key Insight Extraction Approach

This is **not academic research** - aim for directionally correct insights, not perfect statistical rigor:
- Focus on actionable intelligence over academic rigor
- Use representative quotes to validate quantitative findings
- Triangulate across multiple questions to build confidence
- Validate themes with stakeholders, not just data

The goal is strategic intelligence that drives organizational transformation, not a peer-reviewed research paper.
