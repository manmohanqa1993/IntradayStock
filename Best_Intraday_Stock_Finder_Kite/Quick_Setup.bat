@echo off
color 0A
echo ========================================
echo  QUICK SETUP WIZARD
echo  Kite Edition - Real-time Data
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
    echo Try running manually: pip install kiteconnect pandas numpy
    echo.
) else (
    echo.
    echo [PASS] Packages installed successfully
)

echo.
echo ========================================
echo.

REM Step 3: Kite API Configuration
echo Step 3: Kite API Configuration
echo.
echo ========================================
echo KITE CONNECT API REQUIRED
echo ========================================
echo.
echo ⚡ Real-time data (0 seconds delay)
echo 📊 5-minute candles with live updates
echo 🎯 Exact entry/exit timing
echo 💰 Cost: Rs. 2,000/month (Zerodha charges)
echo.
echo Steps to get API credentials:
echo 1. Visit: https://developers.kite.trade/
echo 2. Login with Zerodha credentials
echo 3. Create new app
echo 4. Get API Key and API Secret
echo 5. Add them to config.py
echo.
echo Do you want to open config.py now? (y/n)
set /p opencfg=

if /i "%opencfg%"=="y" (
    notepad config.py
    echo.
    echo After adding your API key and secret, save and close.
    echo.
    pause
)

echo.
echo ========================================
echo.

REM Step 4: First Login
echo Step 4: Kite Login (Generate Access Token)
echo.
echo You need to login to Kite to generate access token.
echo This must be done daily (token expires at 3:30 PM).
echo.
echo Do you want to login now? (y/n)
set /p dologin=

if /i "%dologin%"=="y" (
    echo.
    echo Starting login process...
    echo Follow the instructions in the console.
    echo.
    pause
    python -c "from kite_data_handler import KiteDataHandler; from config import get_kite_config; handler = KiteDataHandler(get_kite_config()); handler.connect()"
    echo.
    echo IMPORTANT: Copy the access token shown above
    echo and save it to config.py
    echo.
    pause
)

echo.
echo ========================================
echo.

REM Step 5: Optional Telegram
echo Step 5: Telegram Alerts (Optional)
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
echo 1. Make sure config.py has your Kite credentials
echo 2. Make sure access token is saved (re-login daily)
echo 3. Double-click Run_Scanner.bat to start
echo.
echo Files you can run:
echo - Run_Scanner.bat           : Start the scanner
echo - Kite_Login.bat            : Daily login for token
echo - Test_Kite_Connection.bat  : Test Kite API
echo - View_Signals.bat          : See generated signals
echo - View_Logs.bat             : Check error logs
echo.
echo IMPORTANT: Access token expires daily at 3:30 PM
echo            Run Kite_Login.bat each morning
echo.
pause
