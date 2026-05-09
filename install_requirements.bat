@echo off
echo ========================================
echo  INSTALLING REQUIRED PACKAGES
echo ========================================
echo.
echo This will install all required Python packages...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install packages
echo Installing required packages...
echo This may take 2-5 minutes depending on your internet speed...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ========================================
    echo  INSTALLATION FAILED
    echo ========================================
    echo.
    echo Please try manual installation:
    echo   pip install yfinance
    echo   pip install pandas
    echo   pip install numpy
    echo   pip install requests
    echo   pip install beautifulsoup4
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  INSTALLATION SUCCESSFUL!
echo ========================================
echo.

REM Verify installation
echo Verifying installation...
python -c "import yfinance, pandas, numpy, requests; print('✅ All core packages installed!')"

if errorlevel 1 (
    echo.
    echo ⚠️ Verification failed. Some packages may not be installed correctly.
    echo Please check the error messages above.
    echo.
) else (
    echo.
    echo ✅ All packages installed and verified!
    echo.
    echo You can now run:
    echo   - python intraday_scanner_pro.py
    echo   - python backtest_advanced.py
    echo   - Or double-click the .bat files
    echo.
)

pause
