@echo off
title ADGM Corporate Agent Pro - Setup

echo 🏢 ADGM Corporate Agent Pro - Setup Script
echo ==========================================
echo.

:: Check Python version
echo 🔍 Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+ first.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set python_version=%%i
echo ✅ Python %python_version% detected

:: Create virtual environment
echo.
echo 🔧 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created successfully

:: Activate virtual environment
echo.
echo 🚀 Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo.
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

:: Create launcher script
echo.
echo 📝 Creating launcher script...
echo @echo off > launch.bat
echo title ADGM Corporate Agent Pro >> launch.bat
echo echo 🚀 Starting ADGM Corporate Agent Pro... >> launch.bat
echo call venv\Scripts\activate.bat >> launch.bat
echo streamlit run app.py --server.port 8501 >> launch.bat

echo.
echo 🎉 Setup completed successfully!
echo.
echo To start the application:
echo   launch.bat
echo.
echo Or manually:
echo   venv\Scripts\activate.bat
echo   streamlit run app.py
echo.
echo 📱 The application will be available at: http://localhost:8501
echo.
pause
