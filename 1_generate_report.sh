#!/bin/bash
# SC Survey Analyzer - Generate Insights Report
# This script runs the automated report generator

echo "================================================"
echo "  SC Survey Analyzer - Report Generator"
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

# Run the report generator
echo "Generating insights report from survey data..."
python generate_insights.py

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "  Report generated successfully!"
    echo "  Check INSIGHTS_REPORT_LATEST.txt"
    echo "================================================"
else
    echo ""
    echo "ERROR: Report generation failed!"
    exit 1
fi

# Keep terminal open
read -p "Press Enter to exit..."
