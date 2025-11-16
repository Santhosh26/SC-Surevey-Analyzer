@echo off
REM SC Survey Analyzer - First-Time Setup Script (Windows)
REM This script creates a virtual environment and installs all dependencies

echo ================================================
echo   SC Survey Analyzer - Setup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if venv already exists
if exist "venv\" (
    echo Virtual environment already exists.
    set /p RECREATE="Do you want to recreate it? (y/N): "
    if /i not "%RECREATE%"=="y" (
        echo Setup cancelled.
        pause
        exit /b 0
    )
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

REM Download NLTK data
echo.
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('brown', quiet=True)"

echo.
echo ================================================
echo   Setup completed successfully!
echo ================================================
echo.
echo You can now use:
echo   1_GENERATE_REPORT.bat - to generate insights report
echo   2_LAUNCH_DASHBOARD.bat - to launch the web dashboard
echo.
pause
