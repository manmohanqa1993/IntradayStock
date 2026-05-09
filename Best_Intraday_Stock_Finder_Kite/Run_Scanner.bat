@echo off
color 0A
echo ========================================
echo  BEST INTRADAY STOCK FINDER
echo  Kite Edition - Real-time Data
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo Run Install_Requirements.bat first
    pause
    exit /b 1
)

echo Starting Kite Scanner...
echo.
echo Press Ctrl+C to stop scanning
echo.

python Best_Intraday_Stock_Finder_Kite.py

echo.
echo Scanner stopped
pause
