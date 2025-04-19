import yfinance as yf
import pandas as pd
import datetime as dt


def get_data(symbol, start_date=dt.datetime(2010, 1, 1)):
    start = {
        '^BVSP': dt.datetime(1996, 1, 1),
        '^GSPC': dt.datetime(1910, 1, 1),
        '^IXIC': dt.datetime(1910, 1, 1)
    }
    
    # Get the appropriate start date for the symbol or use the provided one
    effective_start_date = start.get(symbol, start_date)
    
    # Download data with auto_adjust=False to get Adjusted Close
    data = yf.download(symbol, start=effective_start_date, end=dt.datetime.now(), auto_adjust=False, interval='1d')
    
    # Reset index to make Date a column
    data = data.reset_index()
    
    # Rename columns to match expected format
    data = data.rename(columns={
        'Date': 'd',
        'High': 'high',
        'Low': 'low',
        'Close': 'value',  # Using Close instead of Adj Close
        'Open': 'open',
        'Volume': 'volume'
    })
    
    # Create a clean DataFrame with just the required columns
    x = pd.DataFrame()
    x['d'] = data['d']
    x['value'] = data['value']
    
    # Ensure date is in datetime format
    x['d'] = pd.to_datetime(x['d'])
    
    print(f"Downloaded {len(x)} rows of data for {symbol}")
    
    return x

def process_data(data):
    data['delta'] = data['close'].diff()
    data['delta'] = data['delta'].fillna(0)
    data['delta'] = data['close'] / (data['close'] - data['delta'])

    return data
