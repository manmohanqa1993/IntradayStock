@echo off
echo Opening signals output folder...
if exist "signals_output" (
    explorer signals_output
) else (
    echo Signals folder doesn't exist yet
    echo Run the scanner first to generate signals
    pause
)
