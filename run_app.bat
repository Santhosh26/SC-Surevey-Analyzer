@echo off
echo ========================================
echo Presales Survey Analysis Dashboard
echo ========================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Starting Streamlit dashboard...
echo.
echo The dashboard will open in your default browser.
echo Press CTRL+C to stop the server.
echo.
streamlit run app.py
