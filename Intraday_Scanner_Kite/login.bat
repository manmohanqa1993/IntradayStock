@echo off
echo ========================================
echo  KITE LOGIN
echo  Generate Access Token (Daily)
echo ========================================
echo.
python -c "import sys; sys.path.insert(0, 'src'); sys.path.insert(0, 'config'); from data_handler import KiteDataHandler; from settings import get_kite_config; handler = KiteDataHandler(get_kite_config()); handler.connect()"
echo.
pause
