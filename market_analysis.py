import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.dates import YearLocator, DateFormatter
import warnings
import datetime as dt

# Suppress warnings
warnings.filterwarnings("ignore")

def create_sp500_chart():
    """Create an improved S&P 500 chart"""
    print("Downloading S&P 500 data...")
    
    try:
        # Download data
        data = yf.download("^GSPC", start="1990-01-01", auto_adjust=False)
        print(f"Downloaded {len(data)} days of data")
        
        # Create figure with better size for display
        plt.figure(figsize=(12, 6), dpi=100)
        
        # Plot the price data with improved styling
        plt.plot(data.index, data['Close'], color='#1f77b4', linewidth=1.5)
        
        # Add grid with more subtle styling
        plt.grid(alpha=0.3, linestyle='--')
        
        # Add title and labels with improved fonts
        plt.title('S&P 500 Historical Performance', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        
        # Format x-axis to show years
        plt.gca().xaxis.set_major_locator(YearLocator(5))  # Show every 5 years
        plt.gca().xaxis.set_major_formatter(DateFormatter('%Y'))
        plt.xticks(rotation=45)
        
        # Use log scale for better perspective on long-term growth
        plt.yscale('log')
        
        # Highlight key market events with markers and annotations
        events = {
            "Dot-com Crash": {"date": "2000-03-24", "color": "#ff7f0e"},
            "2008 Crisis": {"date": "2008-09-15", "color": "#d62728"},
            "COVID-19": {"date": "2020-03-16", "color": "#9467bd"},
        }
        
        for name, info in events.items():
            date = pd.to_datetime(info['date'])
            if date >= data.index[0] and date <= data.index[-1]:
                closest_idx = data.index.get_indexer([date], method='nearest')[0]
                price = data['Close'].iloc[closest_idx]
                
                # Add marker
                plt.scatter(date, price, s=80, color=info['color'], zorder=5)
                
                # Add annotation with arrow
                plt.annotate(name, 
                            xy=(date, price),
                            xytext=(0, 30),  # Points above the point
                            textcoords='offset points',
                            ha='center',
                            arrowprops=dict(arrowstyle='->', color=info['color']),
                            bbox=dict(boxstyle='round,pad=0.3', alpha=0.7, fc='white'))
        
        # Remove spines to improve appearance
        for spine in ['top', 'right']:
            plt.gca().spines[spine].set_visible(False)
        
        # Save the chart with improved resolution
        plt.tight_layout()
        plt.savefig('sp500_history.png', dpi=120, bbox_inches='tight')
        print("Chart saved as sp500_history.png")
        plt.show()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_sp500_chart()