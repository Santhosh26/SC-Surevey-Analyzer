#!/bin/bash
# SC Survey Analyzer - PyInstaller Build Script (Mac/Linux)
# This script creates a standalone executable

echo "================================================"
echo "  SC Survey Analyzer - Executable Builder"
echo "================================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if PyInstaller is installed
python -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
if [ -d "build" ]; then
    echo "Cleaning previous build artifacts..."
    rm -rf build
fi
if [ -d "dist" ]; then
    rm -rf dist
fi

# Build the executable
echo ""
echo "Building standalone executable..."
echo "This may take several minutes..."
echo ""
pyinstaller app.spec --clean

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed!"
    exit 1
fi

echo ""
echo "================================================"
echo "  Build completed successfully!"
echo "================================================"
echo ""
echo "Executable location: dist/SC_Survey_Analyzer/"
echo ""
echo "To run the app:"
echo "  1. Copy the entire 'dist/SC_Survey_Analyzer' folder to target machine"
echo "  2. Run ./SC_Survey_Analyzer"
echo ""
echo "Note: The first run may take longer as it initializes."
echo ""
