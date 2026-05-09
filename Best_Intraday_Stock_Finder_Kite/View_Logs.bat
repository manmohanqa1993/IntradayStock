@echo off
echo Opening log file...
if exist "logs\kite_scanner.log" (
    notepad logs\kite_scanner.log
) else (
    echo Log file doesn't exist yet
    echo Run the scanner first to generate logs
    pause
)
