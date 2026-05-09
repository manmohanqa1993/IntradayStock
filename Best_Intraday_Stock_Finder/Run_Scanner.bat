@echo off
echo ========================================
echo  BEST INTRADAY STOCK FINDER
echo  F&O Momentum Continuation Scanner
echo ========================================
echo.
echo Starting scanner...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Run the scanner
python Best_Intraday_Stock_Finder.py

echo.
echo ========================================
echo Scanner stopped
echo ========================================
pause
