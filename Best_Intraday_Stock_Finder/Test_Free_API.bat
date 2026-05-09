@echo off
echo ========================================
echo  Testing FREE Yahoo Finance API
echo  No API Keys Required!
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

echo Testing free data connection...
echo.

python -c "import yfinance as yf; ticker = yf.Ticker('RELIANCE.NS'); data = ticker.history(period='1d', interval='5m'); print('✅ FREE API Working!'); print(f'RELIANCE Price: ₹{data[\"Close\"].iloc[-1]:.2f}'); print(f'Candles Today: {len(data)}')"

if errorlevel 1 (
    echo.
    echo ❌ yfinance not installed
    echo Installing now...
    pip install yfinance
    echo.
    echo Run this test again
) else (
    echo.
    echo ========================================
    echo ✅ FREE API is working perfectly!
    echo ========================================
    echo.
    echo You can now run the scanner:
    echo   Double-click Run_Scanner.bat
)

echo.
pause
