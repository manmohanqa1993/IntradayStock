@echo off
echo ========================================
echo  VIEWING LOG FILES
echo  Best Intraday Stock Finder
echo ========================================
echo.

if exist logs\screener.log (
    echo Opening log file...
    echo.
    notepad logs\screener.log
) else (
    echo No log file found yet.
    echo Run the scanner first to generate logs.
    echo.
    pause
)
