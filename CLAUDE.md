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
- Automatic sentiment classification (Positive/Neutral/Negative) using TextBlob
- Sentiment distribution pie charts
- Most positive and negative response highlights with polarity scores

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

## Key Insight Extraction Approach

This is **not academic research** - aim for directionally correct insights, not perfect statistical rigor:
- Focus on actionable intelligence over academic rigor
- Use representative quotes to validate quantitative findings
- Triangulate across multiple questions to build confidence
- Validate themes with stakeholders, not just data

The goal is strategic intelligence that drives organizational transformation, not a peer-reviewed research paper.
