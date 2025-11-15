@echo off
echo ========================================
echo Generating Insights Report...
echo ========================================
echo.
call venv\Scripts\python.exe generate_insights.py
echo.
echo ========================================
echo Opening report...
echo ========================================
if exist "INSIGHTS_REPORT_LATEST.txt" (
    start "" "INSIGHTS_REPORT_LATEST.txt"
    echo Report opened in your default text editor
) else (
    echo Could not find report file
)
echo.
echo Press any key to exit...
pause >nul
