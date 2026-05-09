@echo off
color 0A
echo ========================================
echo  KITE LOGIN HELPER
echo  Generate Access Token
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

echo This will help you login to Kite and generate access token
echo.

python -c "from kite_data_handler import KiteDataHandler; from config import get_kite_config; handler = KiteDataHandler(get_kite_config()); handler.connect()"

echo.
pause
