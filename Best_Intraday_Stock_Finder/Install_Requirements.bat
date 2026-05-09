@echo off
echo ========================================
echo  INSTALLING DEPENDENCIES
echo  Best Intraday Stock Finder
echo ========================================
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

echo Python found!
echo.
echo Installing required packages...
echo This may take 2-5 minutes depending on your internet speed
echo.

REM Install all requirements
pip install -r requirements.txt

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit config.py and add your broker API credentials
echo 2. Double-click Run_Scanner.bat to start scanning
echo.
pause
