@echo off
echo ========================================
echo  TELEGRAM ALERT TEST
echo  Best Intraday Stock Finder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

echo Testing Telegram connection...
echo.

python alert_system.py

echo.
pause
