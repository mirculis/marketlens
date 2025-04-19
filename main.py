#!/usr/bin/env python3
"""
Financial Market Analysis Tool
------------------------------
This script generates various market analysis charts including:
- Historical market crashes compared to current market conditions
- Market recovery patterns
- Simple price charts with key market events

Usage:
    python main.py --symbol ^GSPC  # For S&P 500
    python main.py --symbol ^BVSP  # For Ibovespa
"""

import argparse
import os
import feeder_yahoo
import process
import cache
import plot
import market_analysis

def create_directories():
    """Create necessary directories for data and images"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('img', exist_ok=True)
    os.makedirs('data/ibov', exist_ok=True)

def run_index_analysis(symbol):
    """Run analysis for a specific market index"""
    print(f"\n=== Running analysis for {symbol} ===\n")
    
    # Get data
    data = feeder_yahoo.get_data(symbol)
    print(data.tail())
    
    # Process crashes
    crashes = process.crashes(data)
    cache.save_crashes(crashes, symbol)
    plot.crashes(crashes, symbol, save=True)
    
    # Process recovery
    recover = process.recover(data)
    plot.recover(recover, symbol, save=True)
    
    print(f"\n=== Analysis complete for {symbol} ===\n")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Financial Market Analysis Tool')
    parser.add_argument('--symbol', type=str, default='^GSPC', 
                        help='Market symbol to analyze (default: ^GSPC for S&P 500)')
    parser.add_argument('--simple', action='store_true',
                        help='Run the simple market analysis visualization')
    
    args = parser.parse_args()
    
    # Create necessary directories
    create_directories()
    
    if args.simple:
        # Run the simple market analysis with modern styling
        print("\n=== Running simple market analysis ===\n")
        market_analysis.create_sp500_chart()
    else:
        # Run the detailed index analysis
        run_index_analysis(args.symbol)

if __name__ == "__main__":
    main()