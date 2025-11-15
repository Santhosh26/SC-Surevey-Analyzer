@echo off
echo ========================================
echo Launching Interactive Dashboard...
echo ========================================
echo.
echo The dashboard will open at:
echo http://localhost:8501
echo.
echo Press CTRL+C to stop the server
echo.
call venv\Scripts\activate.bat
streamlit run app.py
