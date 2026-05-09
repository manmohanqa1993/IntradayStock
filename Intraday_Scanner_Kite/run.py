"""
Intraday Scanner Kite - Zerodha Kite Connect
=============================================
Real-time data from Zerodha Kite API
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from scanner import IntradayStockFinder

def main():
    """Main entry point"""
    print("="*60)
    print(" INTRADAY SCANNER KITE")
    print(" Zerodha Kite Connect API - Real-time Data")
    print("="*60)
    print()

    scanner = IntradayStockFinder()
    scanner.start()

if __name__ == "__main__":
    main()
