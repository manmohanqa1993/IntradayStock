@echo off
color 0A
echo ========================================
echo  Testing Kite Connection
echo  Real-time Data Test
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

echo Testing Kite API connection...
echo.

python -c "from kite_data_handler import KiteDataHandler; from config import get_kite_config; handler = KiteDataHandler(get_kite_config()); success = handler.connect(); print(); print('='*50); print('Testing data fetch for RELIANCE...') if success else None; candles = handler.get_intraday_data('RELIANCE') if success else None; print(f'✅ Fetched {len(candles)} candles') if candles is not None else print('❌ Could not fetch data'); print(f'Latest RELIANCE Price: ₹{candles[\"close\"].iloc[-1]:.2f}') if candles is not None else None; print('='*50) if success else print('Fix the errors above and try again')"

echo.
pause
