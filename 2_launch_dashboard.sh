#!/bin/bash
# SC Survey Analyzer - Launch Streamlit Dashboard
# This script launches the interactive web dashboard

echo "================================================"
echo "  SC Survey Analyzer - Dashboard Launcher"
echo "================================================"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup.sh first to create the environment."
    exit 1
fi

# Download NLTK data if not already present
echo "Checking NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('brown', quiet=True)" > /dev/null 2>&1

# Launch Streamlit app
echo ""
echo "Launching Streamlit dashboard..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

streamlit run app.py
