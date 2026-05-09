@echo off
color 0A
echo ========================================
echo  Installing Python Packages
echo  Kite Edition
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo.
    echo Please install Python first:
    echo 1. Download from https://www.python.org/downloads/
    echo 2. During installation, CHECK "Add Python to PATH"
    echo 3. Restart computer
    echo 4. Run this script again
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

echo Installing packages from requirements.txt...
echo This may take 2-5 minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Some packages may have failed to install
    echo Try running: pip install kiteconnect pandas numpy
) else (
    echo.
    echo ========================================
    echo Packages installed successfully!
    echo ========================================
)

echo.
pause
