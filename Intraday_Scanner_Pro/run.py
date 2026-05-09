"""
Intraday Scanner Pro - Professional Version
===========================================
Hybrid NSE + Yahoo Finance (Best FREE setup)
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from scanner import IntradayScanner

def main():
    """Main entry point"""
    print("="*60)
    print(" INTRADAY SCANNER PRO - PROFESSIONAL VERSION")
    print(" Hybrid NSE Official + Yahoo Finance")
    print("="*60)
    print()

    scanner = IntradayScanner()
    scanner.start()

if __name__ == "__main__":
    main()
