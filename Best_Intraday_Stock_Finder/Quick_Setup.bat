@echo off
color 0A
echo ========================================
echo  QUICK SETUP WIZARD
echo  Best Intraday Stock Finder
echo ========================================
echo.

REM Step 1: Check Python
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python is NOT installed
    echo.
    echo Please install Python first:
    echo 1. Download from https://www.python.org/downloads/
    echo 2. Run installer
    echo 3. CHECK "Add Python to PATH" during installation
    echo 4. Restart computer
    echo 5. Run this setup again
    echo.
    pause
    exit /b 1
) else (
    echo [PASS] Python is installed
    python --version
)

echo.
echo ========================================
echo.

REM Step 2: Install packages
echo Step 2: Installing Python packages...
echo This will take 2-5 minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARNING] Some packages may have failed to install
    echo This is usually okay - scanner will still work
    echo.
) else (
    echo.
    echo [PASS] Packages installed successfully
)

echo.
echo ========================================
echo.

REM Step 3: Data Source
echo Step 3: Data Source Configuration
echo.
echo ========================================
echo GREAT NEWS: Scanner uses HYBRID NSE+Yahoo (FREE!)
echo ========================================
echo.
echo ✅ NO API keys needed
echo ✅ NO broker account required
echo ✅ Works immediately!
echo ✅ NSE Official daily data (most accurate)
echo ✅ Yahoo Finance 5-min candles
echo ⚠️  15-20 minute data delay
echo.
echo Perfect for:
echo   - Learning the strategy
echo   - Paper trading
echo   - Backtesting
echo.
echo Want real-time data for live trading?
echo   1. Open config.py
echo   2. Change BROKER = "zerodha" (or your broker)
echo   3. Add API credentials
echo.
echo Configure broker now? (y/n)
set /p opencfg=

if /i "%opencfg%"=="y" (
    notepad config.py
) else (
    echo.
    echo Using FREE Hybrid NSE+Yahoo - No configuration needed!
)

echo.
echo ========================================
echo.

REM Step 4: Optional Telegram
echo Step 4: Telegram Alerts (Optional)
echo.
echo Do you want to setup Telegram alerts? (y/n)
set /p telegram=

if /i "%telegram%"=="y" (
    echo.
    echo Telegram Setup Instructions:
    echo 1. Open Telegram, search @BotFather
    echo 2. Send /newbot and follow instructions
    echo 3. Copy your Bot Token
    echo 4. Search @userinfobot to get your Chat ID
    echo 5. Update config.py:
    echo    - ENABLE_TELEGRAM = True
    echo    - TELEGRAM_BOT_TOKEN = 'your_token'
    echo    - TELEGRAM_CHAT_ID = 'your_chat_id'
    echo.
    echo Open config.py to add Telegram credentials? (y/n)
    set /p opentg=
    if /i "%opentg%"=="y" (
        notepad config.py
    )
)

echo.
echo ========================================
echo  SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure config.py has your broker credentials
echo 2. Double-click Run_Scanner.bat to start
echo.
echo Files you can run:
echo - Run_Scanner.bat         : Start the scanner
echo - Test_Telegram.bat       : Test Telegram alerts
echo - View_Signals.bat        : See generated signals
echo - View_Logs.bat           : Check error logs
echo.
pause
