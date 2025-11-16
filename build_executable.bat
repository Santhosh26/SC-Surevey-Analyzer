@echo off
REM SC Survey Analyzer - PyInstaller Build Script (Windows)
REM This script creates a standalone executable

echo ================================================
echo   SC Survey Analyzer - Executable Builder
echo ================================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Clean previous builds
if exist "build\" (
    echo Cleaning previous build artifacts...
    rmdir /s /q build
)
if exist "dist\" (
    rmdir /s /q dist
)

REM Build the executable
echo.
echo Building standalone executable...
echo This may take several minutes...
echo.
pyinstaller app.spec --clean

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Build completed successfully!
echo ================================================
echo.
echo Executable location: dist\SC_Survey_Analyzer\
echo.
echo To run the app:
echo   1. Copy the entire 'dist\SC_Survey_Analyzer' folder to target machine
echo   2. Double-click SC_Survey_Analyzer.exe
echo.
echo Note: The first run may take longer as it initializes.
echo.
pause
