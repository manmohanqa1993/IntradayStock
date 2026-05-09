@echo off
echo ========================================
echo  SETUP - INTRADAY SCANNER KITE
echo ========================================
echo.
echo Installing Kite Connect requirements...
pip install -r requirements.txt
echo.
echo ========================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Get Kite API key from https://developers.kite.trade/
echo 2. Edit config/settings.py - add API credentials
echo 3. Run: login.bat (daily login)
echo 4. Run: run.bat (start scanner)
echo ========================================
pause
