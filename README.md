# Financial Market Analysis Tool

A Python-based toolkit for analyzing and visualizing financial market data, with a focus on market crashes, recoveries, and historical comparisons.

## Features

- **Historical Crash Analysis**: Compare current market conditions against historical market crashes
- **Recovery Patterns**: Visualize how markets have recovered after major downturns
- **Modern Visualizations**: Create clean, informative financial charts with proper styling
- **Multiple Index Support**: Analyze different market indices (S&P 500, Ibovespa, etc.)
- **Data Caching**: Save processed data for faster reuse and analysis

## Running Locally

Here's how to run the financial market analysis tool locally:

1. **Clone the repository to your local machine** (or download files if not from a git repository)

2. **Set up a Python virtual environment:**
   ```bash
   # Navigate to the project directory
   cd /path/to/test-project

   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories** (if they don't exist already):
   ```bash
   mkdir -p data img data/ibov
   ```

5. **Run the analysis:**

   **Basic usage** (analyzes S&P 500 by default):
   ```bash
   python main.py
   ```

   **For a simpler, modern visualization:**
   ```bash
   python main.py --simple
   ```

   **To analyze a different market index:**
   ```bash
   python main.py --symbol ^BVSP  # For Brazilian Ibovespa
   ```

6. **View the generated charts:**
   - Check the `img/` directory for output charts:
     - `crash_sp500.png`: Historical crashes comparison
     - `recovery_sp500.png`: Market recovery patterns

7. **Help menu:**
   ```bash
   python main.py --help
   ```

## Output

The tool generates various charts in the `img/` directory:

- `crash_sp500.png`: Historical crashes compared to current market conditions
- `recovery_sp500.png`: Market recovery patterns after bottoms
- `sp500_history.png`: Simple historical chart with key market events highlighted

## Project Structure

- `main.py`: Main entry point for the application
- `feeder_yahoo.py`: Data fetching from Yahoo Finance
- `process.py`: Data processing functions
- `plot.py`: Chart generation functions
- `cache.py`: Data caching utilities
- `market_analysis.py`: Modern visualization alternatives

## Features of Enhanced Visualizations

### Crash Chart Improvements
- Better color scheme with highlighted current crash
- Visual hierarchy with varying line weights and opacities
- Clear labeling of significant events
- Reference grid lines with percentage markers
- Professional typography and layout

### Recovery Chart Improvements
- Color-coded categorization of recovery types
- Clear marking of market bottoms
- Improved scaling and readability
- Professional styling and consistent visual language
- Intuitive legend to explain the different patterns

## Credits

This tool uses the following open-source packages:
- [yfinance](https://github.com/ranaroussi/yfinance)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/)

## License

[MIT License](LICENSE)