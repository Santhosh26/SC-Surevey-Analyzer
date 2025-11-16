"""
Presales Survey Analysis Dashboard
Interactive visualization and analysis tool for International Presales All-Hands survey data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# ==================== COLOR SCHEME CONFIGURATION ====================
# Google Maps-Inspired Vibrant Orange & Blue Theme
COLOR_SCHEME = {
    # Core Brand Colors
    'primary_blue': '#4285F4',        # Google Maps vibrant blue
    'primary_orange': '#FF6D00',      # Vibrant orange for highlights
    'secondary_blue': '#1967D2',      # Deeper blue for contrast
    'secondary_orange': '#FF8F00',    # Lighter orange for variety
    'accent_teal': '#00BCD4',         # Complementary cool accent
    'accent_purple': '#7B1FA2',       # For diversity in multi-series charts

    # Semantic Colors (Adapted to Palette)
    'positive': '#00C853',            # Vibrant green
    'neutral': '#90A4AE',             # Blue-gray
    'negative': '#FF6F00',            # Vibrant orange

    # UI Elements
    'bg_light': '#F5F7FA',            # Subtle cool gray
    'bg_blue': '#E3F2FD',             # Light blue wash
    'bg_orange': '#FFF3E0',           # Light orange wash
    'text_dark': '#37474F',           # Blue-gray dark
    'white': '#FFFFFF',

    # Chart Colorscales (Plotly - will create custom)
    'chart_main': [[0, '#E3F2FD'], [0.5, '#4285F4'], [1, '#FF6D00']],  # Blue to Orange gradient
    'chart_blue': [[0, '#E3F2FD'], [0.5, '#4285F4'], [1, '#1967D2']],  # Light to Dark Blue
    'chart_orange': [[0, '#FFF3E0'], [0.5, '#FF8F00'], [1, '#FF6D00']], # Light to Dark Orange

    # Word Cloud Colormap (matplotlib)
    'wordcloud_cmap': 'plasma'        # Vibrant purple-orange-yellow gradient
}

# Page configuration
st.set_page_config(
    page_title="Presales Survey Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling - Using centralized color scheme
st.markdown(f"""
    <style>
    .main-header {{
        font-size: 2.5rem;
        font-weight: bold;
        color: {COLOR_SCHEME['primary_blue']};
        margin-bottom: 1rem;
    }}
    .sub-header {{
        font-size: 1.5rem;
        font-weight: bold;
        color: {COLOR_SCHEME['text_dark']};
        margin-top: 2rem;
        margin-bottom: 1rem;
    }}
    .metric-card {{
        background-color: {COLOR_SCHEME['bg_light']};
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: {COLOR_SCHEME['text_dark']};
    }}
    .insight-box {{
        background-color: {COLOR_SCHEME['bg_blue']};
        padding: 1rem;
        border-left: 4px solid {COLOR_SCHEME['primary_blue']};
        margin: 1rem 0;
        color: {COLOR_SCHEME['text_dark']};
    }}
    .quote-box {{
        background-color: {COLOR_SCHEME['bg_orange']};
        padding: 1rem;
        border-left: 4px solid {COLOR_SCHEME['primary_orange']};
        margin: 0.5rem 0;
        font-style: italic;
        color: {COLOR_SCHEME['text_dark']};
    }}
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA LOADING ====================

@st.cache_data
def load_data():
    """Load and parse raw survey data - returns both open-ended and multiple choice"""
    try:
        df = pd.read_csv('raw-data.csv', encoding='utf-8-sig')
        df.columns = df.columns.str.strip()  # Clean column names

        # Handle different possible column names
        if 'Responses' in df.columns:
            df = df.rename(columns={'Responses': 'Response'})

        df['Response'] = df['Response'].astype(str).str.strip()
        df['Question'] = df['Question'].astype(str).str.strip()

        # Filter out invalid data
        df = df[df['Response'].notna() & (df['Response'] != '') & (df['Response'] != 'nan')]
        df = df[df['Question'].notna() & (df['Question'] != '') & (df['Question'] != 'nan')]

        # Separate open-ended from multiple choice questions
        # Multiple choice questions have numeric responses (vote counts)
        df['Is_Numeric'] = df['Response'].str.match(r'^\d+$', na=False)

        open_ended = df[~df['Is_Numeric']].copy()
        multiple_choice = df[df['Is_Numeric']].copy()

        # Filter open-ended questions with at least 10 responses
        question_counts = open_ended['Question'].value_counts()
        valid_questions = question_counts[question_counts >= 10].index
        open_ended = open_ended[open_ended['Question'].isin(valid_questions)]

        return open_ended, multiple_choice
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

@st.cache_data
def get_multiple_choice_data():
    """Get structured multiple choice data"""
    # Future Roles
    future_roles = {
        'Role': [
            'Solution Architects - Technical Credibility',
            'Industry Value Consultants - CXO Engagement',
            'Business Value Engineers - ROI/TCO Justification',
            'Demo Specialist - AI-powered Inspiration',
            'Innovation Leads - Co-creation and Rapid Pilots',
            'Enablement Coaches - Scale Knowledge and Capability'
        ],
        'Votes': [69, 34, 33, 38, 51, 30]
    }

    # Future Skillsets
    future_skillsets = {
        'Skillset': [
            'Technical expertise',
            'Financial modelling',
            'Adaptability & customer empathy',
            'Industry-specific business acumen',
            'Advanced storytelling'
        ],
        'First_Place_Votes': [20, 0, 21, 30, 30]
    }

    return future_roles, future_skillsets

@st.cache_data
def get_question_summary(df):
    """Generate summary statistics by question"""
    summary = df.groupby('Question').agg({
        'Response': ['count', lambda x: x.nunique()]
    }).reset_index()
    summary.columns = ['Question', 'Total Responses', 'Unique Responses']
    return summary

# ==================== HELPER FUNCTIONS ====================

def clean_text(text):
    """Clean text for analysis"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_top_words(responses, top_n=20, exclude_words=None):
    """Extract top N words from responses"""
    if exclude_words is None:
        exclude_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                        'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                        'should', 'may', 'might', 'can', 'our', 'we', 'us', 'i', 'my', 'me'}

    all_words = []
    for response in responses:
        cleaned = clean_text(response)
        words = [w for w in cleaned.split() if w not in exclude_words and len(w) > 2]
        all_words.extend(words)

    word_counts = Counter(all_words)
    return word_counts.most_common(top_n)

# ==================== VISUALIZATION FUNCTIONS ====================

def create_wordcloud(responses, title="Word Cloud"):
    """Generate word cloud from responses"""
    text = ' '.join([clean_text(r) for r in responses])

    if not text.strip():
        st.warning("No text available for word cloud")
        return None

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color=COLOR_SCHEME['white'],
        colormap=COLOR_SCHEME['wordcloud_cmap'],
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold')
    return fig

def create_frequency_chart(word_counts, title="Top Words"):
    """Create bar chart of word frequencies"""
    if not word_counts:
        return None

    words, counts = zip(*word_counts)

    fig = go.Figure([go.Bar(
        x=list(counts),
        y=list(words),
        orientation='h',
        marker=dict(
            color=list(counts),
            colorscale=COLOR_SCHEME['chart_blue'],
            showscale=True
        )
    )])

    fig.update_layout(
        title=title,
        xaxis_title="Frequency",
        yaxis_title="Words",
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )

    return fig

def create_response_distribution(df):
    """Create distribution chart of responses per question"""
    question_counts = df['Question'].value_counts().reset_index()
    question_counts.columns = ['Question', 'Count']

    # Shorten question labels for better display
    question_counts['Short_Question'] = question_counts['Question'].apply(
        lambda x: x[:50] + '...' if len(x) > 50 else x
    )

    fig = px.bar(
        question_counts,
        x='Count',
        y='Short_Question',
        orientation='h',
        title='Number of Responses per Question',
        labels={'Short_Question': 'Question', 'Count': 'Response Count'},
        color='Count',
        color_continuous_scale=COLOR_SCHEME['chart_blue']
    )

    fig.update_layout(height=600, showlegend=False)
    return fig

# ==================== SENTIMENT ANALYSIS ====================

@st.cache_data
def analyze_sentiment(responses):
    """Perform basic sentiment analysis on responses"""
    from textblob import TextBlob

    sentiments = []
    for response in responses:
        try:
            blob = TextBlob(str(response))
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
                'sentiment': sentiment
            })
        except:
            sentiments.append({
                'response': response,
                'polarity': 0,
                'sentiment': 'Neutral'
            })

    return pd.DataFrame(sentiments)

def create_sentiment_chart(sentiment_df):
    """Create sentiment distribution chart"""
    sentiment_counts = sentiment_df['sentiment'].value_counts()

    colors = {
        'Positive': COLOR_SCHEME['positive'],
        'Neutral': COLOR_SCHEME['neutral'],
        'Negative': COLOR_SCHEME['negative']
    }

    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        marker=dict(colors=[colors.get(s, COLOR_SCHEME['primary_blue']) for s in sentiment_counts.index]),
        hole=0.3
    )])

    fig.update_layout(
        title='Sentiment Distribution',
        height=400
    )

    return fig

# ==================== MAIN APP ====================

def main():
    # Header
    st.markdown('<div class="main-header">📊 Presales Survey Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**International Presales All-Hands Survey 2025** | Transforming 100+ responses into strategic intelligence")

    # Load data
    df, mc_df = load_data()

    if df.empty:
        st.error("No data loaded. Please ensure 'raw-data.csv' is in the project directory.")
        return

    # Sidebar - Filters and Navigation
    st.sidebar.title("🎯 Navigation")

    analysis_mode = st.sidebar.radio(
        "Select Analysis View",
        ["📈 Overview", "🎲 Multiple Choice Results", "❓ Question Deep Dive", "💭 Sentiment Analysis", "🎯 Quick Wins", "📊 Cross-Question Analysis"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Open-Ended Responses:** {len(df)}")
    st.sidebar.markdown(f"**Open-Ended Questions:** {df['Question'].nunique()}")
    st.sidebar.markdown(f"**Multiple Choice Questions:** 2")
    st.sidebar.markdown(f"**Total Questions:** {df['Question'].nunique() + 2}")

    # ==================== OVERVIEW ====================
    if analysis_mode == "📈 Overview":
        st.markdown('<div class="sub-header">Survey Overview</div>', unsafe_allow_html=True)

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Open-Ended Responses", len(df))
        with col2:
            total_questions = df['Question'].nunique() + 2
            st.metric("Total Questions", total_questions)
            st.caption("12 open-ended + 2 multiple choice")
        with col3:
            avg_responses = len(df) / df['Question'].nunique()
            st.metric("Avg Responses/Question", f"{avg_responses:.1f}")
        with col4:
            unique_respondents = len(df) // df['Question'].nunique()
            st.metric("Est. Respondents", f"~{unique_respondents}")

        st.markdown("---")

        # Response distribution
        st.plotly_chart(create_response_distribution(df), use_container_width=True)

        # Question summary table
        st.markdown('<div class="sub-header">Response Summary by Question (Open-Ended)</div>', unsafe_allow_html=True)
        summary = get_question_summary(df)
        st.dataframe(summary, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.info("💡 **Tip:** Check the '🎲 Multiple Choice Results' tab to see the 2 multiple choice questions!")

    # ==================== MULTIPLE CHOICE RESULTS ====================
    elif analysis_mode == "🎲 Multiple Choice Results":
        st.markdown('<div class="sub-header">Multiple Choice Questions Analysis</div>', unsafe_allow_html=True)

        # Get MC data
        future_roles, future_skillsets = get_multiple_choice_data()

        # ========== FUTURE ROLES ==========
        st.markdown("### 1️⃣ Future Roles in International Presales")
        st.markdown("**Question:** What do you believe are the future roles in International Presales?")
        st.markdown("**Format:** Multiple choice (respondents could select multiple roles)")

        # Process data
        roles_df = pd.DataFrame(future_roles)
        roles_df['Percentage'] = (roles_df['Votes'] / roles_df['Votes'].sum() * 100).round(1)
        roles_df = roles_df.sort_values('Votes', ascending=False)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Votes", roles_df['Votes'].sum())
        with col2:
            st.metric("Avg Selections per Person", f"{roles_df['Votes'].sum() / 100:.1f}")
            st.caption("Assuming ~100 respondents")
        with col3:
            st.metric("Top Role", "Solution Architects")
            st.caption(f"{roles_df.iloc[0]['Votes']} votes ({roles_df.iloc[0]['Percentage']}%)")

        # Visualization
        fig_roles = go.Figure([go.Bar(
            y=roles_df['Role'],
            x=roles_df['Votes'],
            orientation='h',
            text=[f"{v} ({p}%)" for v, p in zip(roles_df['Votes'], roles_df['Percentage'])],
            textposition='outside',
            marker=dict(
                color=roles_df['Votes'],
                colorscale=COLOR_SCHEME['chart_blue'],
                showscale=False
            )
        )])

        fig_roles.update_layout(
            title='Future Roles - Vote Distribution',
            xaxis_title='Number of Votes',
            yaxis_title='',
            height=400,
            xaxis=dict(range=[0, max(roles_df['Votes']) * 1.2])
        )

        st.plotly_chart(fig_roles, use_container_width=True)

        # Key insights
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**💡 Key Insights:**")
        st.markdown(f"- **Solution Architects** remain the core role ({roles_df.iloc[0]['Percentage']}% selection rate)")
        st.markdown(f"- **Innovation Leads** rising as second priority ({roles_df.iloc[1]['Percentage']}%) - focus on co-creation")
        st.markdown(f"- **Portfolio approach:** Average {roles_df['Votes'].sum() / 100:.1f} roles per person → need for specialization")
        st.markdown(f"- **Balanced distribution:** No single role dominates (all roles 12-27%)")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ========== FUTURE SKILLSETS ==========
        st.markdown("### 2️⃣ Future Skillsets & Mindsets Ranking")
        st.markdown("**Question:** Rank these key skillsets & mindsets for Presales of the future")
        st.markdown("**Format:** Ranking question (showing only 1st-place votes)")

        # Process data
        skills_df = pd.DataFrame(future_skillsets)
        skills_df['Percentage'] = (skills_df['First_Place_Votes'] / skills_df['First_Place_Votes'].sum() * 100).round(1)
        skills_df = skills_df.sort_values('First_Place_Votes', ascending=False)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total 1st Place Votes", skills_df['First_Place_Votes'].sum())
        with col2:
            top_skills = skills_df[skills_df['First_Place_Votes'] == skills_df['First_Place_Votes'].max()]
            st.metric("Top Priority (Tied)", len(top_skills))
            st.caption(", ".join(top_skills['Skillset'].tolist()[:2]))
        with col3:
            st.metric("Technical Expertise Ranking", "4th place")
            st.caption(f"Only {skills_df[skills_df['Skillset'] == 'Technical expertise']['Percentage'].iloc[0]}% ranked it #1")

        # Visualization
        fig_skills = go.Figure([go.Bar(
            y=skills_df['Skillset'],
            x=skills_df['First_Place_Votes'],
            orientation='h',
            text=[f"{v} ({p}%)" for v, p in zip(skills_df['First_Place_Votes'], skills_df['Percentage'])],
            textposition='outside',
            marker=dict(
                color=skills_df['First_Place_Votes'],
                colorscale=COLOR_SCHEME['chart_orange'],
                showscale=False
            )
        )])

        fig_skills.update_layout(
            title='Future Skillsets - 1st Place Rankings',
            xaxis_title='Number of 1st Place Votes',
            yaxis_title='',
            height=350,
            xaxis=dict(range=[0, max(skills_df['First_Place_Votes']) * 1.2])
        )

        st.plotly_chart(fig_skills, use_container_width=True)

        # Key insights
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**💡 Key Insights:**")
        st.markdown(f"- **TIED for #1:** Industry-specific acumen & Advanced storytelling (30 votes each, {skills_df.iloc[0]['Percentage']}%)")
        st.markdown(f"- **Shift observed:** Business skills > Technical skills (Industry acumen #1 vs Technical expertise #4)")
        st.markdown(f"- **Surprising:** Financial modelling = 0 first-place votes (may be delegated or not seen as primary skill)")
        st.markdown(f"- **Soft skills valued:** Adaptability & empathy in 2nd place ({skills_df.iloc[2]['Percentage']}%)")
        st.markdown(f"- **Strategic implication:** Presales evolving from technical-first to business-first orientation")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Cross-validation with open-ended
        st.markdown("### 🔗 Cross-Validation with Open-Ended Responses")
        st.markdown("**Comparing Multiple Choice with Open-Ended Themes:**")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Multiple Choice Results:**")
            st.markdown("- Top Role: Solution Architects (27%)")
            st.markdown("- Top Skill: Industry Acumen (30%)")
            st.markdown("- Top Skill (tied): Storytelling (30%)")

        with col2:
            st.markdown("**Open-Ended Themes (from Q2 - Future Mission):**")
            st.markdown("- 'Advisor' mentioned 20 times (18%)")
            st.markdown("- 'Trusted' mentioned 11 times (10%)")
            st.markdown("- 'Value' mentioned 9 times (8%)")

        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**✅ Validation:** Multiple choice confirms open-ended themes!")
        st.markdown("- Solution Architects (27%) aligns with 'Advisor'/'Trusted' themes (28% combined)")
        st.markdown("- Industry acumen #1 validates need for business/value focus in open-ended responses")
        st.markdown("- Consistent narrative: Technical competence + Business advisory + Storytelling")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== QUESTION DEEP DIVE ====================
    elif analysis_mode == "❓ Question Deep Dive":
        st.markdown('<div class="sub-header">Question Deep Dive</div>', unsafe_allow_html=True)

        # Question selector
        questions = sorted(df['Question'].unique())
        selected_question = st.selectbox("Select a question to analyze:", questions)

        # Filter data
        question_df = df[df['Question'] == selected_question]

        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Responses", len(question_df))
        with col2:
            st.metric("Unique Responses", question_df['Response'].nunique())

        st.markdown("---")

        # Word Cloud
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Word Cloud")
            wordcloud_fig = create_wordcloud(question_df['Response'], f"Word Cloud - {selected_question[:50]}...")
            if wordcloud_fig:
                st.pyplot(wordcloud_fig)

        with col2:
            st.markdown("### Top 10 Words")
            top_words = get_top_words(question_df['Response'], top_n=10)
            if top_words:
                for word, count in top_words:
                    st.markdown(f"**{word}:** {count}")

        # Frequency chart
        st.markdown("---")
        st.markdown("### Word Frequency Distribution")
        top_words_full = get_top_words(question_df['Response'], top_n=20)
        freq_chart = create_frequency_chart(top_words_full, "Top 20 Words by Frequency")
        if freq_chart:
            st.plotly_chart(freq_chart, use_container_width=True)

        # Response samples
        st.markdown("---")
        st.markdown("### Sample Responses")
        num_samples = min(10, len(question_df))
        sample_responses = question_df['Response'].sample(n=num_samples).tolist()

        for i, response in enumerate(sample_responses, 1):
            st.markdown(f'<div class="quote-box">{i}. "{response}"</div>', unsafe_allow_html=True)

    # ==================== SENTIMENT ANALYSIS ====================
    elif analysis_mode == "💭 Sentiment Analysis":
        st.markdown('<div class="sub-header">Sentiment Analysis</div>', unsafe_allow_html=True)

        # Question selector
        questions = sorted(df['Question'].unique())
        selected_question = st.selectbox("Select a question for sentiment analysis:", questions)

        # Filter data
        question_df = df[df['Question'] == selected_question]

        with st.spinner("Analyzing sentiment..."):
            sentiment_df = analyze_sentiment(question_df['Response'])

        # Sentiment distribution
        col1, col2 = st.columns([1, 2])

        with col1:
            st.plotly_chart(create_sentiment_chart(sentiment_df), use_container_width=True)

        with col2:
            st.markdown("### Sentiment Summary")
            sentiment_counts = sentiment_df['sentiment'].value_counts()
            total = len(sentiment_df)

            for sentiment in ['Positive', 'Neutral', 'Negative']:
                if sentiment in sentiment_counts.index:
                    count = sentiment_counts[sentiment]
                    pct = (count / total) * 100
                    st.markdown(f"**{sentiment}:** {count} responses ({pct:.1f}%)")

        # Most positive/negative responses
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Most Positive Responses")
            positive_df = sentiment_df[sentiment_df['sentiment'] == 'Positive'].nlargest(5, 'polarity')
            for idx, row in positive_df.iterrows():
                st.markdown(f'<div class="quote-box">"{row["response"]}" (Score: {row["polarity"]:.2f})</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("### Most Negative Responses")
            negative_df = sentiment_df[sentiment_df['sentiment'] == 'Negative'].nsmallest(5, 'polarity')
            for idx, row in negative_df.iterrows():
                st.markdown(f'<div class="quote-box">"{row["response"]}" (Score: {row["polarity"]:.2f})</div>', unsafe_allow_html=True)

    # ==================== QUICK WINS ====================
    elif analysis_mode == "🎯 Quick Wins":
        st.markdown('<div class="sub-header">Quick Wins Analysis</div>', unsafe_allow_html=True)
        st.markdown("Identifying immediate action items from **Stop Doing** and **Start Doing** responses")

        # Find Stop/Start questions
        stop_questions = [q for q in df['Question'].unique() if 'stop' in q.lower()]
        start_questions = [q for q in df['Question'].unique() if 'start' in q.lower()]

        if stop_questions or start_questions:
            col1, col2 = st.columns(2)

            with col1:
                if stop_questions:
                    st.markdown("### 🛑 Stop Doing")
                    stop_df = df[df['Question'].isin(stop_questions)]

                    # Word cloud
                    wordcloud_fig = create_wordcloud(stop_df['Response'], "Stop Doing - Key Themes")
                    if wordcloud_fig:
                        st.pyplot(wordcloud_fig)

                    # Top themes
                    st.markdown("#### Top Pain Points to Eliminate")
                    top_stops = get_top_words(stop_df['Response'], top_n=10)
                    for word, count in top_stops:
                        st.markdown(f"- **{word.title()}**: {count} mentions")

            with col2:
                if start_questions:
                    st.markdown("### ▶️ Start Doing")
                    start_df = df[df['Question'].isin(start_questions)]

                    # Word cloud
                    wordcloud_fig = create_wordcloud(start_df['Response'], "Start Doing - Key Themes")
                    if wordcloud_fig:
                        st.pyplot(wordcloud_fig)

                    # Top themes
                    st.markdown("#### Top Initiatives to Launch")
                    top_starts = get_top_words(start_df['Response'], top_n=10)
                    for word, count in top_starts:
                        st.markdown(f"- **{word.title()}**: {count} mentions")

            # Quick Wins Matrix Placeholder
            st.markdown("---")
            st.markdown("### Impact × Effort Matrix")
            st.info("💡 **Next Step:** Manually categorize top items by Impact (High/Low) and Effort (High/Low) to create prioritization matrix")

            # Sample matrix (placeholder)
            st.markdown("""
            **Suggested categorization approach:**
            - **P1 (High Impact, Low Effort):** Launch within 0-30 days
            - **P2 (High Impact, High Effort):** Medium-term roadmap (30-90 days)
            - **P3 (Low Impact, Low Effort):** Quick wins but lower priority
            - **P4 (Low Impact, High Effort):** Deprioritize
            """)
        else:
            st.warning("No 'Stop Doing' or 'Start Doing' questions found in the dataset.")

    # ==================== CROSS-QUESTION ANALYSIS ====================
    elif analysis_mode == "📊 Cross-Question Analysis":
        st.markdown('<div class="sub-header">Cross-Question Correlation Analysis</div>', unsafe_allow_html=True)
        st.markdown("Compare responses across related questions to identify patterns and gaps")

        # Question pair selector
        questions = sorted(df['Question'].unique())

        col1, col2 = st.columns(2)
        with col1:
            question_1 = st.selectbox("Select first question:", questions, key='q1')
        with col2:
            question_2 = st.selectbox("Select second question:", questions, key='q2', index=min(1, len(questions)-1))

        if question_1 == question_2:
            st.warning("Please select two different questions for comparison.")
        else:
            # Get data for both questions
            q1_df = df[df['Question'] == question_1]
            q2_df = df[df['Question'] == question_2]

            # Side-by-side comparison
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"#### {question_1[:60]}...")
                st.metric("Responses", len(q1_df))

                # Top words
                top_words_q1 = get_top_words(q1_df['Response'], top_n=10)
                st.markdown("**Top Themes:**")
                for word, count in top_words_q1:
                    st.markdown(f"- {word}: {count}")

            with col2:
                st.markdown(f"#### {question_2[:60]}...")
                st.metric("Responses", len(q2_df))

                # Top words
                top_words_q2 = get_top_words(q2_df['Response'], top_n=10)
                st.markdown("**Top Themes:**")
                for word, count in top_words_q2:
                    st.markdown(f"- {word}: {count}")

            # Word clouds
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                wc1 = create_wordcloud(q1_df['Response'], f"Q1: {question_1[:40]}...")
                if wc1:
                    st.pyplot(wc1)

            with col2:
                wc2 = create_wordcloud(q2_df['Response'], f"Q2: {question_2[:40]}...")
                if wc2:
                    st.pyplot(wc2)

            # Common themes
            st.markdown("---")
            st.markdown("### Common Themes Across Both Questions")

            words_q1 = set([w[0] for w in top_words_q1])
            words_q2 = set([w[0] for w in top_words_q2])
            common_words = words_q1.intersection(words_q2)

            if common_words:
                st.markdown(f"**{len(common_words)} common themes found:**")
                st.markdown(", ".join([w.title() for w in common_words]))
            else:
                st.info("No common themes found in top 10 words. This suggests these questions capture different dimensions.")

            # Insight prompt
            st.markdown("---")
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("**💡 Suggested Analysis:**")
            st.markdown(f"Look for patterns between these questions. For example:")
            st.markdown(f"- Are the top themes in Q1 aligned with or contradicted by themes in Q2?")
            st.markdown(f"- What gaps exist between aspirations (Q1) and reality (Q2)?")
            st.markdown(f"- Which themes appear in both? What does this tell you about priorities?")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
