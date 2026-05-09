@echo off
echo ========================================
echo  OPENING SIGNALS OUTPUT FOLDER
echo  Best Intraday Stock Finder
echo ========================================
echo.

if exist signals_output (
    echo Opening signals folder...
    explorer signals_output
) else (
    echo No signals folder found yet.
    echo Folder will be created when scanner runs.
    echo.
    pause
)
