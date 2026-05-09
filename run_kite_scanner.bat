@echo off
echo ========================================
echo  KITE (ZERODHA) INTRADAY SCANNER
echo ========================================
echo.
echo Real-time data from Zerodha Kite API
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

echo Running Kite scanner...
echo.
python intraday_scanner_kite.py

echo.
echo ========================================
echo Scan complete!
echo ========================================
pause
