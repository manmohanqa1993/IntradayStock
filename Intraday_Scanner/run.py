"""
Intraday Scanner - Basic Version
=================================
Simple, beginner-friendly scanner using Yahoo Finance (FREE)
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scanner import IntradayScanner

def main():
    """Main entry point"""
    print("="*60)
    print(" INTRADAY SCANNER - BASIC VERSION")
    print(" FREE Yahoo Finance Data")
    print("="*60)
    print()

    scanner = IntradayScanner()
    scanner.start()

if __name__ == "__main__":
    main()
