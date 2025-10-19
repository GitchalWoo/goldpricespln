#!/usr/bin/env python3
"""
NBP Gold Price Data Downloader

This script fetches historical gold prices from the National Bank of Poland (NBP) API
and aggregates them to monthly averages, saving the results to a JSON file.

NBP API: https://api.nbp.pl/api/cenyzlota/
- Gold price data available from: 2013-01-02
- Daily granularity with prices in PLN per gram (1000 proof)
- API limit: 93 days per request

Usage:
    python fetch_nbp_gold_prices.py [--start-year 2013] [--output ../data/nbp-gold-prices.json]
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
import sys


class NBPGoldPriceFetcher:
    """Fetches and processes gold price data from NBP API."""
    
    BASE_URL = "https://api.nbp.pl/api/cenyzlota"
    API_LIMIT_DAYS = 93  # NBP API returns max 93 days per request
    EARLIEST_DATA = datetime(2013, 1, 2)  # Earliest available data from NBP
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def fetch_price_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Fetch gold prices for a date range from NBP API.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of dicts with 'date' and 'price' keys
        """
        url = f"{self.BASE_URL}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}/"
        
        self.log(f"Fetching: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            prices = []
            
            for entry in data:
                prices.append({
                    'date': entry['data'],  # Note: NBP uses 'data' key for date
                    'price': float(entry['cena'])  # 'cena' is the price in PLN
                })
            
            self.log(f"  Retrieved {len(prices)} daily prices")
            return prices
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch data for {start_date} to {end_date}: {e}", file=sys.stderr)
            return []
    
    def fetch_all_data(self, start_year: int = 2013) -> List[Dict]:
        """
        Fetch all available gold price data from NBP.
        
        Args:
            start_year: Starting year (default: 2013, earliest NBP data)
            
        Returns:
            List of dicts with daily price data sorted by date
        """
        all_prices = []
        
        # Start from the beginning of the start_year
        current_start = datetime(start_year, 1, 1)
        current_start = max(current_start, self.EARLIEST_DATA)
        
        today = datetime.now()
        
        self.log(f"Fetching NBP gold prices from {current_start.strftime('%Y-%m-%d')} to today")
        
        while current_start < today:
            # Calculate end date (93 days later or today, whichever is earlier)
            current_end = current_start + timedelta(days=self.API_LIMIT_DAYS)
            current_end = min(current_end, today)
            
            prices = self.fetch_price_range(current_start, current_end)
            all_prices.extend(prices)
            
            # Move to next range (avoiding gaps)
            current_start = current_end + timedelta(days=1)
        
        # Sort by date
        all_prices.sort(key=lambda x: x['date'])
        
        self.log(f"Total daily prices retrieved: {len(all_prices)}")
        return all_prices
    
    def aggregate_to_monthly(self, daily_prices: List[Dict]) -> List[Dict]:
        """
        Aggregate daily prices to monthly averages.
        
        Args:
            daily_prices: List of dicts with 'date' and 'price' keys
            
        Returns:
            List of dicts with 'year', 'month', and 'price' keys (monthly average)
        """
        monthly_data = {}
        
        for entry in daily_prices:
            date_obj = datetime.strptime(entry['date'], '%Y-%m-%d')
            year_month = date_obj.strftime('%Y-%m')
            
            if year_month not in monthly_data:
                monthly_data[year_month] = []
            
            monthly_data[year_month].append(entry['price'])
        
        # Calculate averages and format output
        monthly_prices = []
        for year_month in sorted(monthly_data.keys()):
            prices = monthly_data[year_month]
            avg_price = sum(prices) / len(prices)
            
            year, month = year_month.split('-')
            monthly_prices.append({
                'year': int(year),
                'month': int(month),
                'price': round(avg_price, 2)
            })
        
        self.log(f"Aggregated to {len(monthly_prices)} monthly data points")
        return monthly_prices
    
    def to_yearly_average(self, monthly_prices: List[Dict]) -> List[Dict]:
        """
        Convert monthly prices to yearly averages (for compatibility with existing format).
        
        Args:
            monthly_prices: List of dicts with 'year', 'month', and 'price' keys
            
        Returns:
            List of dicts with 'year' and 'price' keys (yearly average)
        """
        yearly_data = {}
        
        for entry in monthly_prices:
            year = entry['year']
            if year not in yearly_data:
                yearly_data[year] = []
            yearly_data[year].append(entry['price'])
        
        yearly_prices = []
        for year in sorted(yearly_data.keys()):
            prices = yearly_data[year]
            avg_price = sum(prices) / len(prices)
            yearly_prices.append({
                'year': year,
                'price': round(avg_price, 2)
            })
        
        return yearly_prices
    
    def save_json(self, data: List[Dict], filepath: Path, pretty: bool = True):
        """
        Save data to JSON file.
        
        Args:
            data: Data to save
            filepath: Output file path
            pretty: Whether to pretty-print JSON
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2 if pretty else None, ensure_ascii=False)
        
        self.log(f"Saved {len(data)} entries to {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch gold prices from NBP API and save to JSON file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch all data and save as yearly averages (default)
  python fetch_nbp_gold_prices.py

  # Fetch data starting from 2015
  python fetch_nbp_gold_prices.py --start-year 2015

  # Save as monthly data
  python fetch_nbp_gold_prices.py --monthly

  # Verbose output
  python fetch_nbp_gold_prices.py -v
        """
    )
    
    parser.add_argument(
        '--start-year',
        type=int,
        default=2013,
        help='Starting year for data retrieval (default: 2013, earliest NBP data)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path(__file__).parent.parent / 'data' / 'nbp-gold-prices.json',
        help='Output JSON file path (default: ../data/nbp-gold-prices.json)'
    )
    parser.add_argument(
        '--monthly',
        action='store_true',
        help='Save monthly data instead of yearly average'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print(f"NBP Gold Price Downloader")
    print(f"{'=' * 50}")
    
    fetcher = NBPGoldPriceFetcher(verbose=args.verbose)
    
    try:
        # Fetch all daily prices
        daily_prices = fetcher.fetch_all_data(start_year=args.start_year)
        
        if not daily_prices:
            print("[ERROR] No data retrieved from NBP API", file=sys.stderr)
            return 1
        
        print(f"\nData Processing:")
        print(f"{'=' * 50}")
        
        if args.monthly:
            # Save monthly data
            monthly_prices = fetcher.aggregate_to_monthly(daily_prices)
            fetcher.save_json(monthly_prices, args.output)
            print(f"[OK] Monthly data saved: {len(monthly_prices)} entries")
        else:
            # Save yearly average (default, for backward compatibility)
            yearly_prices = fetcher.aggregate_to_monthly(daily_prices)
            yearly_prices = fetcher.to_yearly_average(yearly_prices)
            fetcher.save_json(yearly_prices, args.output)
            print(f"[OK] Yearly data saved: {len(yearly_prices)} entries")
        
        print(f"\nOutput: {args.output.resolve()}")
        print(f"Done!")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
