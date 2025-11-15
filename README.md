# Presales Survey Analysis Toolkit

Transform 100+ survey responses into strategic intelligence and actionable insights.

---

## 🚀 Quick Start

### Step 1: Generate Insights Report (5 seconds)
```bash
Double-click: 1_GENERATE_REPORT.bat
```
- Analyzes all 1,415 responses automatically
- Opens `INSIGHTS_REPORT_LATEST.txt` with all findings
- Top themes, quick wins, cross-question patterns, executive summary

### Step 2: Explore Visually (optional)
```bash
Double-click: 2_LAUNCH_DASHBOARD.bat
```
- Opens interactive web app at http://localhost:8501
- Word clouds, sentiment analysis, export charts
- 5 views: Overview, Deep Dive, Sentiment, Quick Wins, Cross-Question

---

## 📊 Your Data

**Survey Responses:**
- 1,415 valid responses
- 12 questions analyzed
- ~118 respondents

**Key Insights Preview:**
- Team Culture: 21.8% "collaborative", 13.5% "supportive"
- Future Mission: 28% "trusted advisor" theme (clear consensus)
- AI Adoption: 175 responses on tools (high engagement)
- Quick Wins: High-frequency stop/start items ready for action

---

## 📁 Project Files

### Main Tools
- **`1_GENERATE_REPORT.bat`** - Generate insights report (start here)
- **`2_LAUNCH_DASHBOARD.bat`** - Launch web app
- **`generate_insights.py`** - Automated analysis engine
- **`app.py`** - Interactive Streamlit dashboard

### Data
- **`raw-data.csv`** - Survey responses (1,415 responses)
- **`INSIGHTS_REPORT_LATEST.txt`** - Latest analysis report
- **`presales_survey_analysis.xlsx`** - Excel workbook (optional)

### Methodology Guides
- **`README_START_HERE.md`** - 4-week analysis roadmap
- **`Thematic_Coding_Framework.md`** - Analysis methodology
- **`Quick_Wins_Guide.md`** - Prioritization framework
- **`Executive_Summary_Template.md`** - Report structure

### Configuration
- **`requirements.txt`** - Python dependencies
- **`venv/`** - Virtual environment (pre-configured)
- **`.gitignore`** - Git exclusions

---

## 📈 Recommended Workflow

### Day 1: Generate & Review (2 hours)
1. Run `1_GENERATE_REPORT.bat`
2. Read insights report (30 min)
3. Run `2_LAUNCH_DASHBOARD.bat`
4. Explore all 5 views (1 hour)
5. Export 5 key charts (15 min)

### Day 2-3: Deep Analysis (4 hours)
- Run sentiment analysis per question
- Identify cross-question patterns
- Export 10-15 charts for presentation

### Day 4-5: Build Presentation (3 hours)
- Create PowerPoint with exported charts
- Write executive summary
- Prioritize quick wins (2×2 matrix)

### Day 6-7: Finalize (2 hours)
- Practice presentation
- Launch first quick win

---

## 📊 Exporting Charts from Web App

1. Right-click any Plotly chart → "Download plot as PNG"
2. Word clouds: Right-click → "Save image as..."
3. Camera icon (top-right of interactive charts)

**Best charts for presentations:**
- Team Culture word cloud
- Future Mission word cloud
- Stop Doing frequency bar chart
- Start Doing frequency bar chart
- AI Tools adoption chart

---

## 🔍 What's in the Insights Report

`INSIGHTS_REPORT_LATEST.txt` contains:

- **Overview** - Total responses, questions analyzed
- **Q1-Q12 Analysis** - Top 15 themes per question with frequencies
- **Quick Wins** - High-priority stop/start items (>5% mention rate)
- **AI Gap Analysis** - Desired vs current AI usage
- **Strategic Tensions** - Vision vs reality patterns
- **Executive Summary** - Key takeaways for leadership

**Read time:** 15 minutes full | 3 minutes executive summary only

---

## 🛠️ Troubleshooting

### Web app won't start
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### No data loaded
- Ensure `raw-data.csv` is in project directory
- Check CSV has "Question,Responses" header

### Sentiment analysis errors
```bash
venv\Scripts\python.exe -m textblob.download_corpora
```

---

## 📚 Additional Resources

- **`QUICK_START.md`** - Detailed quick start guide
- **`CLAUDE.md`** - Technical architecture
- **Methodology guides** - See files above

---

## 💡 Key Features

✅ Automated theme extraction (top 15 per question)
✅ Sentiment analysis (positive/neutral/negative)
✅ Word clouds and frequency charts
✅ Cross-question correlation analysis
✅ Quick wins identification (high-frequency items)
✅ Export-ready visualizations
✅ Executive summary generation

---

**Built with:** Python, Streamlit, Plotly, TextBlob, WordCloud

**Purpose:** Transform survey responses into strategic intelligence for presales team transformation (2025-2027)
