# Presales Survey Analysis Toolkit

Transform survey responses into strategic intelligence and actionable insights through interactive data visualization and sentiment analysis.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Create virtual environment:**
```bash
python -m venv venv
```

2. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download TextBlob corpora (required for sentiment analysis):**
```bash
python -m textblob.download_corpora
```

### Launch Dashboard

```bash
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`

---

## 📊 Dashboard Features

### 1. Overview (📈)
- Total response metrics and distribution
- Response counts per question
- Summary statistics table

### 2. Multiple Choice Results (🎲)
- Future roles in presales (vote distribution)
- Future skillsets ranking analysis
- Cross-validation with open-ended responses

### 3. Question Deep Dive (❓)
- Interactive word clouds
- Top word frequency analysis
- Bar charts of word distribution
- Sample responses for qualitative review

### 4. Sentiment Analysis (💭)
- **Question-aware contextual sentiment classification**
- Automatic classification: Positive/Neutral/Negative with confidence scores
- Three-column display: Most Positive, Most Neutral, Most Negative responses
- Sentiment distribution pie charts
- Understands survey context (e.g., "more collaboration" = gap/need, not positive)
- Handles edge cases: listening gaps, constructive "stop" suggestions, POC context

### 5. Quick Wins Analysis (🎯)
- Dedicated view for "Stop Doing" and "Start Doing" questions
- Side-by-side word clouds
- Top pain points and initiatives ranked by frequency
- Impact × Effort matrix framework for prioritization

### 6. Cross-Question Correlation (📊)
- Compare any two questions side-by-side
- Identify common themes across questions
- Spot gaps between aspiration vs reality

---

## 📁 Project Files

### Core Application
- **`app.py`** - Streamlit interactive dashboard
- **`raw-data.csv`** - Survey responses from Menti.com export
- **`requirements.txt`** - Python dependencies

### Documentation
- **`README.md`** - This file (getting started guide)
- **`CLAUDE.md`** - Technical documentation for AI assistants
- **`Future plan.md`** - Roadmap and future enhancements

### Environment
- **`venv/`** - Python virtual environment (created during setup)

---

## 📈 Exporting Charts

All visualizations can be exported for presentations:

1. **Plotly charts:** Right-click → "Download plot as PNG"
2. **Word clouds:** Right-click → "Save image as..."

**Recommended charts for presentations:**
- Team Culture word cloud
- Future Mission word cloud
- Stop Doing frequency bar chart
- Start Doing frequency bar chart
- Sentiment distribution pie charts

---

## 🧠 Sentiment Analysis

The dashboard includes **Question-Aware Sentiment Analysis** that understands survey context beyond simple word polarity.

### How It Works

**Traditional approach (TextBlob only):**
- "More collaboration" → Positive ❌ (missed that "more" indicates a gap)
- "Listen more" → Positive ❌ (missed that it's a missing behavior)

**Question-Aware approach:**
- "More collaboration" → Neutral ✅ (detects gap indicator)
- "Listen more" → Negative ✅ (detects listening gap)
- "POC" in Stop Doing → Negative ✅ (uses question context)

### Features

✅ **Question Context Awareness** - Questions asking "Stop Doing" default negative, "Start Doing" default positive
✅ **Gap Indicator Detection** - "more X", "better X", "need X" patterns indicate missing capabilities
✅ **Negation Handling** - "not enough", "no X", "stop X" recognized as negative signals
✅ **Domain Keywords** - Presales-specific pain points vs strengths
✅ **Confidence Scores** - Shows certainty of classification (0.0-1.0)
✅ **Reasoning Display** - Explains why each response was classified

---

## 🛠️ Troubleshooting

### Dependencies not installing
```bash
# Ensure pip is up to date
python -m pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt
```

### Dashboard won't start
```bash
# Check if virtual environment is activated (should see (venv) in prompt)
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Then launch
streamlit run app.py
```

### No data loaded
- Ensure `raw-data.csv` exists in project directory
- Verify CSV has "Question,Response" or "Question,Responses" header
- Check file encoding is UTF-8

### Sentiment analysis errors
```bash
# Download required TextBlob corpora
python -m textblob.download_corpora
```

### Port already in use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

## 💡 Analysis Workflow

### Step 1: Explore Overview (15 min)
- Review total responses and distribution
- Identify questions with high/low engagement
- Check multiple choice results for quick insights

### Step 2: Deep Dive by Question (1-2 hours)
- Use Question Deep Dive to explore word clouds
- Note top themes per question
- Export word clouds for presentation

### Step 3: Sentiment Analysis (30 min)
- Run sentiment analysis on key questions
- Focus on questions with mixed sentiment
- Note high-confidence negative responses (action items)

### Step 4: Quick Wins Extraction (1 hour)
- Analyze Stop Doing and Start Doing questions
- Identify high-frequency pain points (>10% mention rate)
- Prioritize using Impact × Effort matrix

### Step 5: Cross-Question Patterns (1 hour)
- Compare related questions (e.g., Q2 Mission vs Q12 Challenges)
- Identify vision vs reality gaps
- Look for consistent themes across questions

### Step 6: Create Presentation (2-3 hours)
- Export 10-15 key charts
- Write executive summary with insights
- Create action plan from quick wins

---

## 🎯 Quick Wins Prioritization

Use 2×2 Impact × Effort matrix:

- **P1 (High Impact, Low Effort):** Launch within 0-30 days
- **P2 (High Impact, High Effort):** Medium-term roadmap (30-90 days)
- **P3 (Low Impact, Low Effort):** Quick wins but lower priority
- **P4 (Low Impact, High Effort):** Deprioritize or eliminate

**Frequency thresholds:**
- **High frequency:** >30% of respondents (urgent)
- **Medium frequency:** 15-30% of respondents (important)
- **Low frequency:** <15% of respondents (nice-to-have)

---

## 🔍 Data Format

The toolkit expects CSV data in this format:

```
Question,Response
"How would you describe our team culture?","Collaborative"
"How would you describe our team culture?","Supportive and innovative"
"What is our future mission?","Trusted advisor to customers"
```

**Requirements:**
- Header row: `Question,Response` or `Question,Responses`
- Each row = one response to one question
- Questions are repeated for each response
- Responses can be single words or long-form text
- UTF-8 encoding

---

## 📚 Additional Resources

- **`CLAUDE.md`** - Technical architecture and sentiment analysis details
- **`Future plan.md`** - Planned enhancements and roadmap

---

**Built with:** Python, Streamlit, Plotly, TextBlob, WordCloud

**Purpose:** Transform survey responses into strategic intelligence for presales team transformation (2025-2027)
