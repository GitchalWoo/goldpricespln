#!/usr/bin/env python3
"""
Stock Price Data Downloader

This script fetches historical stock prices from Yahoo Finance (yfinance) for configured
tickers and aggregates them to monthly averages, saving results to individual JSON files.

Each stock gets its own JSON file with monthly data and optional gold equivalent values.

Usage:
    python fetch_stock_prices.py [--config stock-tickers-config.json] [--verbose]
    python fetch_stock_prices.py --help
"""

import json
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import sys
from typing import Dict, List, Tuple, Optional
import warnings

# Suppress yfinance warnings about missing data
warnings.filterwarnings('ignore')


class StockPriceFetcher:
    """Fetches and processes stock price data from Yahoo Finance."""

    def __init__(self, config_path: str = "stock-tickers-config.json", verbose: bool = False):
        """
        Initialize the stock price fetcher.

        Args:
            config_path: Path to the stock tickers configuration JSON file
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.config = self._load_config(config_path)
        self.gold_prices = {}
        self.output_directory = Path(self.config['metadata']['output_directory'])
        self.gold_prices_file = Path(self.config['metadata']['gold_price_file'])

        # Create output directory if it doesn't exist
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            Configuration dictionary
        """
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                # Try relative to scripts directory
                config_file = Path(__file__).parent / config_path

            with open(config_file, 'r') as f:
                self.log(f"Loading configuration from {config_file}")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load config file: {e}", file=sys.stderr)
            sys.exit(1)

    def _load_gold_prices(self) -> bool:
        """
        Load gold prices from nbp-gold-prices-monthly.json.

        Returns:
            True if successful, False otherwise
        """
        try:
            gold_file = Path(self.config['metadata']['gold_price_file'])
            if not gold_file.is_absolute():
                # Make relative to scripts directory
                gold_file = Path(__file__).parent / gold_file

            if not gold_file.exists():
                print(f"[WARN] Gold price file not found: {gold_file}", file=sys.stderr)
                return False

            with open(gold_file, 'r') as f:
                gold_data = json.load(f)
                # Create lookup dict: (year, month) -> price
                self.gold_prices = {(item['year'], item['month']): item['price']
                                    for item in gold_data}
                self.log(f"Loaded {len(self.gold_prices)} gold price entries")
                return True
        except Exception as e:
            print(f"[WARN] Failed to load gold prices: {e}", file=sys.stderr)
            return False

    def fetch_stock_data(self, ticker: str, start_year: int = 2013) -> Optional[Dict]:
        """
        Fetch stock data from Yahoo Finance.

        Args:
            ticker: Stock ticker symbol
            start_year: Start year for data collection

        Returns:
            Dictionary with monthly aggregated data, or None if fetch fails
        """
        try:
            start_date = f"{start_year}-01-01"
            end_date = datetime.now().strftime("%Y-%m-%d")

            self.log(f"Fetching {ticker} from {start_date} to {end_date}")
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if data.empty:
                print(f"[WARN] No data found for ticker: {ticker}", file=sys.stderr)
                return None

            # Aggregate to monthly data (using last trading day of month)
            monthly_data = self._aggregate_to_monthly(data)
            self.log(f"  Retrieved {len(monthly_data)} monthly data points for {ticker}")

            return monthly_data

        except Exception as e:
            print(f"[ERROR] Failed to fetch data for {ticker}: {e}", file=sys.stderr)
            return None

    def _aggregate_to_monthly(self, daily_data) -> List[Dict]:
        """
        Aggregate daily stock data to monthly (using last trading day of month).

        Args:
            daily_data: pandas DataFrame from yfinance

        Returns:
            List of monthly data dictionaries
        """
        monthly_list = []

        # Group by year and month
        daily_data['YearMonth'] = daily_data.index.to_period('M')
        grouped = daily_data.groupby('YearMonth')

        for period, group in grouped:
            # Use the last trading day of the month
            last_day_data = group.iloc[-1]

            month_data = {
                'year': period.year,
                'month': period.month,
                'open': round(float(last_day_data['Open']), 2),
                'high': round(float(group['High'].max()), 2),
                'low': round(float(group['Low'].min()), 2),
                'close': round(float(last_day_data['Close']), 2),
                'volume': int(last_day_data['Volume']) if 'Volume' in last_day_data else None,
            }

            # Add gold equivalent if available
            if (month_data['year'], month_data['month']) in self.gold_prices:
                gold_price_pln = self.gold_prices[(month_data['year'], month_data['month'])]
                month_data['price_gold'] = round(month_data['close'] / gold_price_pln, 2)
            else:
                month_data['price_gold'] = None

            monthly_list.append(month_data)

        return monthly_list

    def save_to_json(self, ticker: str, ticker_name: str, monthly_data: List[Dict]):
        """
        Save monthly data to JSON file.

        Args:
            ticker: Stock ticker symbol
            ticker_name: Human-readable ticker name
            monthly_data: List of monthly data dictionaries
        """
        # Sanitize filename
        filename = ticker.replace('.', '_').replace(' ', '_').lower()
        output_file = self.output_directory / f"{filename}-monthly.json"

        output_data = {
            'ticker': ticker,
            'name': ticker_name,
            'generated': datetime.now().isoformat(),
            'data_points': len(monthly_data),
            'currency': 'PLN' if '.IL' in ticker or '.L' in ticker else 'local',
            'note': 'price_gold values are in grams of gold (1000 proof from NBP)',
            'data': monthly_data
        }

        try:
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            self.log(f"Saved: {output_file}")
            print(f"✅ {ticker}: {output_file} ({len(monthly_data)} months)")
        except Exception as e:
            print(f"[ERROR] Failed to save {ticker} data: {e}", file=sys.stderr)

    def fetch_all_stocks(self):
        """Fetch data for all configured stocks."""
        print("\n📊 Stock Price Downloader\n")
        print(f"Fetching {len(self.config['stocks'])} stocks...\n")

        # Load gold prices once
        gold_loaded = self._load_gold_prices()
        if not gold_loaded:
            print("[WARN] Gold prices not available - price_gold fields will be null\n")

        for stock in self.config['stocks']:
            ticker = stock['ticker']
            name = stock['name']
            start_year = stock.get('start_year', 2013)

            self.log(f"\nProcessing: {ticker} ({name})")

            # Fetch data from Yahoo Finance
            monthly_data = self.fetch_stock_data(ticker, start_year)

            if monthly_data:
                # Save to JSON file
                self.save_to_json(ticker, name, monthly_data)
            else:
                print(f"⚠️  {ticker}: Failed to fetch data")

        print(f"\n✨ All stocks processed!")
        print(f"📁 Output directory: {self.output_directory.absolute()}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch historical stock prices from Yahoo Finance"
    )
    parser.add_argument(
        '--config',
        default='stock-tickers-config.json',
        help='Path to stock tickers configuration file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--help-config',
        action='store_true',
        help='Show configuration file format and exit'
    )

    args = parser.parse_args()

    if args.help_config:
        print("""
Configuration File Format (stock-tickers-config.json):

{
  "stocks": [
    {
      "ticker": "TICKER.IL",
      "name": "Company Name",
      "exchange": "GPW",
      "description": "Description",
      "start_year": 2013
    }
  ],
  "metadata": {
    "gold_price_file": "../data/nbp-gold-prices-monthly.json",
    "output_directory": "../data/stocks/"
  }
}

Ticker Conventions:
- .IL = Warsaw Stock Exchange (GPW)
- .L = London Stock Exchange
- No suffix = NASDAQ/NYSE

For detailed info, see: stock-tickers-config.json
        """)
        sys.exit(0)

    fetcher = StockPriceFetcher(config_path=args.config, verbose=args.verbose)
    fetcher.fetch_all_stocks()


if __name__ == '__main__':
    main()
