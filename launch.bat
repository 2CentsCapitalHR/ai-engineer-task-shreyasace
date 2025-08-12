@echo off
title ADGM Corporate Agent Pro
echo 🚀 Starting ADGM Corporate Agent Pro...
echo ====================================
echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo 🌐 Launching application on http://localhost:8501
echo.
echo 💡 Tips:
echo   - Upload your ADGM documents for analysis
echo   - Navigate through tabs for different features
echo   - Download reports in multiple formats
echo.
echo 🛑 Press Ctrl+C to stop the application
echo.
streamlit run app.py --server.port 8501
