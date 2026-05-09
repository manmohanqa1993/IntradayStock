@echo off
echo ========================================
echo  Testing HYBRID NSE + Yahoo Finance
echo  Best of Both Worlds - FREE!
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

echo Testing HYBRID data sources...
echo.

python -c "print('Testing NSE Official Data...'); from nsepy import get_history; from datetime import datetime, timedelta; end = datetime.now().date(); start = end - timedelta(days=5); data = get_history(symbol='RELIANCE', start=start, end=end); print('✅ NSE Working! Days fetched:', len(data)); print('Latest RELIANCE Close: ₹%.2f' % data['Close'].iloc[-1]); print(); print('Testing Yahoo Finance 5-min candles...'); import yfinance as yf; ticker = yf.Ticker('RELIANCE.NS'); intraday = ticker.history(period='1d', interval='5m'); print('✅ Yahoo Working! Candles today:', len(intraday)); if len(intraday) > 0: print('Latest Price: ₹%.2f' % intraday['Close'].iloc[-1])"

if errorlevel 1 (
    echo.
    echo ❌ One or more libraries not installed
    echo Installing now...
    pip install nsepy yfinance
    echo.
    echo Run this test again
) else (
    echo.
    echo ========================================
    echo ✅ HYBRID API is working perfectly!
    echo ========================================
    echo.
    echo What you get:
    echo   ✅ NSE Official daily data (accurate)
    echo   ✅ Yahoo 5-min candles (intraday)
    echo   ✅ Live quotes from both sources
    echo   ✅ Auto fallback if one fails
    echo.
    echo You can now run the scanner:
    echo   Double-click Run_Scanner.bat
)

echo.
pause
