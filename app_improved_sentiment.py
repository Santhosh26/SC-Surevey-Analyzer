"""
IMPROVED Sentiment Analysis Implementation
Using HuggingFace Transformers instead of TextBlob

To use this version:
1. Install: pip install transformers torch
2. Rename current app.py to app_old.py
3. Rename this file to app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# Import improved sentiment analysis
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    st.warning("⚠️ Transformers not installed. Install with: pip install transformers torch")

# Page configuration
st.set_page_config(
    page_title="Presales Survey Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .quote-box {
        background-color: #fff9e6;
        padding: 1rem;
        border-left: 4px solid #ffa500;
        margin: 0.5rem 0;
        font-style: italic;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA LOADING ====================

@st.cache_data
def load_data():
    """Load and parse raw survey data"""
    try:
        df = pd.read_csv('raw-data.csv', encoding='utf-8-sig')
        df.columns = df.columns.str.strip()

        if 'Responses' in df.columns:
            df = df.rename(columns={'Responses': 'Response'})

        df['Response'] = df['Response'].astype(str).str.strip()
        df['Question'] = df['Question'].astype(str).str.strip()

        df = df[df['Response'].notna() & (df['Response'] != '') & (df['Response'] != 'nan')]
        df = df[df['Question'].notna() & (df['Question'] != '') & (df['Question'] != 'nan')]

        question_counts = df['Question'].value_counts()
        valid_questions = question_counts[question_counts >= 10].index
        df = df[df['Question'].isin(valid_questions)]

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# ==================== IMPROVED SENTIMENT ANALYSIS ====================

@st.cache_resource
def load_sentiment_model():
    """Load transformer-based sentiment model (cached)"""
    if not TRANSFORMERS_AVAILABLE:
        return None

    try:
        # Using DistilBERT - fast and accurate
        model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # CPU (-1) or GPU (0)
        )
        return model
    except Exception as e:
        st.error(f"Error loading sentiment model: {e}")
        return None

def preprocess_response(response):
    """Preprocess response for better sentiment analysis"""
    # Replace underscores with spaces
    response = str(response).replace('_', ' ')

    # Expand common acronyms
    acronym_map = {
        'POC': 'Proof of Concept',
        'AE': 'Account Executive',
        'SE': 'Sales Engineer',
        'AI ': 'Artificial Intelligence ',
        'ROI': 'Return on Investment',
        'TCO': 'Total Cost of Ownership'
    }

    for acronym, expansion in acronym_map.items():
        response = response.replace(acronym, expansion)

    # Add context for very short responses (1-2 words)
    words = response.split()
    if len(words) <= 2:
        # Add minimal context
        response = f"This is described as: {response}"

    return response

def get_question_type(question_text):
    """Determine question type for context-aware analysis"""
    question_lower = question_text.lower()

    if 'stop doing' in question_lower:
        return 'stop_doing'
    elif 'start doing' in question_lower:
        return 'start_doing'
    elif 'challenge' in question_lower or 'bottleneck' in question_lower:
        return 'challenges'
    elif 'culture' in question_lower:
        return 'culture'
    else:
        return 'general'

@st.cache_data
def analyze_sentiment_improved(responses, question_text=""):
    """
    Improved sentiment analysis using transformers

    Args:
        responses: Series of response text
        question_text: Question text for context-aware analysis

    Returns:
        DataFrame with sentiment labels and confidence scores
    """
    model = load_sentiment_model()

    if model is None:
        st.warning("⚠️ Using fallback sentiment analysis. Install transformers for better accuracy.")
        return analyze_sentiment_fallback(responses)

    question_type = get_question_type(question_text)
    sentiments = []

    # Preprocess all responses
    processed_responses = [preprocess_response(r) for r in responses]

    # Batch processing for speed
    try:
        # Process in batches of 32
        batch_size = 32
        results = []

        for i in range(0, len(processed_responses), batch_size):
            batch = processed_responses[i:i+batch_size]
            batch_results = model(batch, truncation=True, max_length=512)
            results.extend(batch_results)

        # Process results
        for original_response, result in zip(responses, results):
            label = result['label']  # 'POSITIVE' or 'NEGATIVE'
            score = result['score']  # Confidence 0-1

            # Map to our categories
            if label == 'POSITIVE':
                sentiment = 'Positive'
                polarity = score
            else:  # NEGATIVE
                sentiment = 'Negative'
                polarity = -score

            # Adjust for question context
            if question_type == 'stop_doing':
                # These are feedback, not necessarily negative
                if sentiment == 'Negative':
                    sentiment = 'Critical Feedback'

            elif question_type == 'challenges':
                # Challenges are informative, not sentiment
                if sentiment == 'Negative':
                    sentiment = 'Challenge Identified'

            sentiments.append({
                'response': original_response,
                'polarity': polarity,
                'sentiment': sentiment,
                'confidence': score
            })

    except Exception as e:
        st.error(f"Error in sentiment analysis: {e}")
        return analyze_sentiment_fallback(responses)

    return pd.DataFrame(sentiments)

def analyze_sentiment_fallback(responses):
    """
    Fallback sentiment analysis using TextBlob
    Used if transformers not available
    """
    from textblob import TextBlob

    sentiments = []
    for response in responses:
        try:
            # Preprocess
            processed = preprocess_response(response)
            blob = TextBlob(processed)
            polarity = blob.sentiment.polarity

            if polarity > 0.1:
                sentiment = 'Positive'
            elif polarity < -0.1:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'

            sentiments.append({
                'response': response,
                'polarity': polarity,
                'sentiment': sentiment,
                'confidence': abs(polarity)
            })
        except:
            sentiments.append({
                'response': response,
                'polarity': 0,
                'sentiment': 'Neutral',
                'confidence': 0
            })

    return pd.DataFrame(sentiments)

# ==================== VISUALIZATION FUNCTIONS ====================

def create_sentiment_chart_improved(sentiment_df):
    """Create improved sentiment distribution chart with confidence"""
    sentiment_counts = sentiment_df['sentiment'].value_counts()

    colors = {
        'Positive': '#2ecc71',
        'Neutral': '#95a5a6',
        'Negative': '#e74c3c',
        'Critical Feedback': '#f39c12',
        'Challenge Identified': '#3498db'
    }

    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        marker=dict(colors=[colors.get(s, '#3498db') for s in sentiment_counts.index]),
        hole=0.3,
        textinfo='label+percent',
        textposition='outside'
    )])

    fig.update_layout(
        title='Sentiment Distribution (Transformer-Based Analysis)',
        height=450,
        showlegend=True
    )

    return fig

def show_confidence_distribution(sentiment_df):
    """Show confidence distribution of predictions"""
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=sentiment_df['confidence'],
        nbinsx=20,
        name='Confidence Distribution',
        marker_color='#3498db'
    ))

    fig.update_layout(
        title='Sentiment Analysis Confidence Distribution',
        xaxis_title='Confidence Score',
        yaxis_title='Count',
        height=300
    )

    return fig

# ==================== COMPARISON FUNCTION ====================

def compare_sentiment_methods(responses, question_text=""):
    """Compare TextBlob vs Transformers side-by-side"""
    st.markdown("### 🔬 Sentiment Analysis Method Comparison")

    # Get both results
    transformer_results = analyze_sentiment_improved(responses, question_text)

    from textblob import TextBlob
    textblob_results = []
    for r in responses:
        try:
            blob = TextBlob(str(r))
            polarity = blob.sentiment.polarity
            sentiment = 'Positive' if polarity > 0.1 else ('Negative' if polarity < -0.1 else 'Neutral')
        except:
            sentiment = 'Neutral'
        textblob_results.append(sentiment)

    # Show comparison
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### TextBlob (Old Method)")
        textblob_counts = pd.Series(textblob_results).value_counts()
        st.write(textblob_counts)

    with col2:
        st.markdown("#### Transformers (New Method)")
        transformer_counts = transformer_results['sentiment'].value_counts()
        st.write(transformer_counts)

    # Show differences
    st.markdown("#### Sample Differences")
    comparison_df = pd.DataFrame({
        'Response': responses.head(20),
        'TextBlob': textblob_results[:20],
        'Transformer': transformer_results['sentiment'].head(20),
        'Confidence': transformer_results['confidence'].head(20).round(3)
    })

    # Highlight differences
    comparison_df['Different'] = comparison_df['TextBlob'] != comparison_df['Transformer']
    st.dataframe(comparison_df[comparison_df['Different']], use_container_width=True)

    return transformer_results, textblob_results

# Note: The rest of the app.py code (main function, other views) would go here
# This is the improved sentiment analysis module

if __name__ == "__main__":
    st.title("Improved Sentiment Analysis - Demo")

    if TRANSFORMERS_AVAILABLE:
        st.success("✅ Transformers library available - using advanced sentiment analysis")
    else:
        st.warning("⚠️ Transformers not available - using TextBlob fallback")
        st.code("pip install transformers torch", language="bash")

    # Test with sample data
    df = load_data()
    if not df.empty:
        question = df['Question'].iloc[0]
        responses = df[df['Question'] == question]['Response'].head(50)

        st.write(f"**Testing on:** {question[:100]}...")
        st.write(f"**Sample size:** {len(responses)} responses")

        if st.button("Run Improved Sentiment Analysis"):
            with st.spinner("Analyzing sentiment..."):
                results = analyze_sentiment_improved(responses, question)

                st.plotly_chart(create_sentiment_chart_improved(results))
                st.plotly_chart(show_confidence_distribution(results))

                st.write("**Sample Results:**")
                st.dataframe(results.head(20), use_container_width=True)
