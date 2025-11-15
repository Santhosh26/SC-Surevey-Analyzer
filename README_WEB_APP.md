# Presales Survey Analysis - Web App

Interactive Streamlit dashboard for analyzing International Presales All-Hands survey data.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download NLTK Data (First Time Only)

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Features

### 📈 Overview Dashboard
- Total response metrics
- Response distribution by question
- Summary statistics table

### ❓ Question Deep Dive
- Interactive word clouds
- Top word frequency analysis
- Bar charts showing word distribution
- Random sample responses for qualitative review

### 💭 Sentiment Analysis
- Automatic sentiment classification (Positive/Neutral/Negative)
- Sentiment distribution pie charts
- Most positive and negative response highlights
- Polarity scores using TextBlob

### 🎯 Quick Wins Analysis
- Dedicated view for "Stop Doing" and "Start Doing" questions
- Side-by-side word clouds
- Top pain points and initiatives ranked by frequency
- Impact × Effort matrix framework for prioritization

### 📊 Cross-Question Correlation
- Compare any two questions side-by-side
- Identify common themes across questions
- Spot gaps between aspiration vs reality
- Suggested analysis prompts

## Data Format

The app expects `raw-data.csv` in the project root with this structure:

```csv
Question,Response
"Question text 1","Response 1"
"Question text 1","Response 2"
"Question text 2","Response 1"
...
```

## Export Capabilities

### Save Visualizations
- Right-click any Plotly chart → "Download plot as PNG"
- Word clouds: Right-click → "Save image as..."

### Export Data
Use the export utilities script (coming soon) to generate:
- PDF reports with all insights
- PowerPoint-ready chart images
- CSV summaries by question

## Deployment Options

### Option 1: Local Presentation
Run locally during presentation:
```bash
streamlit run app.py
```

### Option 2: Streamlit Cloud (Free)
1. Push repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and deploy
4. Share the public URL with stakeholders

### Option 3: Internal Hosting
Deploy to your organization's server using Docker:
```bash
docker build -t presales-survey-app .
docker run -p 8501:8501 presales-survey-app
```

## Customization

### Adjust Word Cloud Settings
Edit `app.py` line ~150:
```python
wordcloud = WordCloud(
    width=800,        # Increase for higher resolution
    height=400,
    max_words=100,    # Adjust max words shown
    colormap='viridis' # Change color scheme: 'Blues', 'Greens', etc.
)
```

### Modify Stopwords
Add domain-specific stopwords in `get_top_words()` function (line ~110):
```python
exclude_words = {'the', 'a', 'and', 'presales', 'team', ...}
```

### Sentiment Threshold
Adjust polarity thresholds in `analyze_sentiment()` (line ~250):
```python
if polarity > 0.1:  # Change to 0.2 for stricter positive classification
    sentiment = 'Positive'
elif polarity < -0.1:  # Change to -0.2 for stricter negative
    sentiment = 'Negative'
```

## Troubleshooting

### "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### NLTK Resource Not Found
```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

### "File not found: raw-data.csv"
Ensure `raw-data.csv` is in the same directory as `app.py`

### Sentiment Analysis Errors
Install TextBlob corpora:
```bash
python -m textblob.download_corpora
```

## Performance Tips

### For Large Datasets (500+ responses)
- Add pagination to sample responses view
- Implement data caching (already enabled with `@st.cache_data`)
- Consider aggregating before visualization

### Speed Up Sentiment Analysis
The sentiment analysis uses caching, so it only runs once per question. If you need to re-run, click the menu (top right) → "Clear cache"

## Next Steps

After exploring the dashboard:
1. Export key charts for PowerPoint presentation
2. Document top themes and insights in Executive Summary
3. Use Quick Wins analysis to identify P1 action items
4. Present cross-question correlations to highlight strategic gaps

## Support

For issues or questions:
- Check the main `README_START_HERE.md` for methodology guidance
- Refer to `Thematic_Coding_Framework.md` for analysis best practices
- Review `CLAUDE.md` for project architecture details
