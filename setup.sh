#!/bin/bash
# SC Survey Analyzer - First-Time Setup Script (Mac/Linux)
# This script creates a virtual environment and installs all dependencies

echo "================================================"
echo "  SC Survey Analyzer - Setup Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    echo ""
    echo "On Mac: brew install python3"
    echo "On Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Check if venv already exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
    read -p "Do you want to recreate it? (y/N): " RECREATE
    if [[ ! "$RECREATE" =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment!"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing required packages..."
echo "This may take a few minutes..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    exit 1
fi

# Download NLTK data
echo ""
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('brown', quiet=True)"

echo ""
echo "================================================"
echo "  Setup completed successfully!"
echo "================================================"
echo ""
echo "You can now use:"
echo "  ./1_generate_report.sh - to generate insights report"
echo "  ./2_launch_dashboard.sh - to launch the web dashboard"
echo ""
