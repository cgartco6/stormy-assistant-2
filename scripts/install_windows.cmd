@echo off
title Stormy Assistant Windows Installer
color 0A

echo ========================================
echo    🌪️  STORMY WINDOWS INSTALLER
echo ========================================
echo.

:: Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  Not running as administrator. Some operations may fail.
    set /p choice="Continue anyway? (y/n): "
    if /i not "!choice!"=="y" exit /b
)

:: Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo ✅ Python found: %%i

:: Create virtual environment
if not exist venv (
    echo 🔹 Creating virtual environment...
    python -m venv venv
)

:: Activate and install
echo 🔹 Installing dependencies...
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install requirements
pip install -r requirements.txt
pip install -r web\requirements-web.txt
pip install -r desktop\requirements-desktop.txt

:: Install PyAudio
pip install pyaudio
if %errorLevel% neq 0 (
    echo ⚠️  PyAudio installation failed. You may need to install manually.
    echo    Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
)

:: Create directories
mkdir data 2>nul
mkdir data\logs 2>nul
mkdir localization\stt_models 2>nul
mkdir localization\tts_voices 2>nul

:: Test microphone
echo 🔹 Testing microphone...
python scripts\test_microphone.py

:: Launch options
echo.
echo Launch Options:
echo 1. Desktop version (full voice)
echo 2. Web version (Flask server)
echo 3. Exit

set /p choice="Enter choice (1-3): "
if "%choice%"=="1" (
    python desktop\main.py
) else if "%choice%"=="2" (
    set /p port="Port (default 5000): "
    if "%port%"=="" set port=5000
    for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do set ip=%%i
    echo 🌐 Server: http://%ip%:%port%
    python web\app.py --host 0.0.0.0 --port %port%
)

echo ✅ Installation complete!
pause
