@echo off
echo ========================================
echo NSE Intraday Live Monitor
echo ========================================
echo.
echo This will scan continuously during market hours
echo Press Ctrl+C to stop
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please follow SETUP_GUIDE.md to install Python first
    echo.
    pause
    exit /b 1
)

echo Starting live monitor...
echo.
python live_monitor.py

pause
