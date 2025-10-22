#!/usr/bin/env python3
"""
NBP Daily Gold Price Fetcher (Last 30 Days)

This script fetches the last 30 days of gold prices from the National Bank of Poland (NBP) API
and saves both the full daily history and the most recent price to separate JSON files.

NBP API: https://api.nbp.pl/api/cenyzlota/
- Gold price data available from: 2013-01-02
- Daily granularity with prices in PLN per gram (1000 proof)
- Fetches last 30 days for historical context

Output files:
- nbp-gold-prices-daily.json: Last 30 days of daily prices
- pricetoday.json: Most recent available price only

Usage:
    python fetch_nbp_gold_price_today.py [--output-daily ../data/nbp-gold-prices-daily.json]
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import sys


class NBPTodayGoldPriceFetcher:
    """Fetches last 30 days of gold prices from NBP API."""
    
    BASE_URL = "https://api.nbp.pl/api/cenyzlota"
    DAYS_TO_FETCH = 30
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def fetch_last_30_days(self) -> List[Dict]:
        """
        Fetch the last 30 days of gold prices from NBP API.
        
        Uses date range endpoint to get multiple days at once.
        NBP only publishes prices on working days, so we request 30 calendar days
        which should give us around 20-22 trading days.
        
        Returns:
            List of dicts with 'date' and 'price' keys, sorted by date (newest first)
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.DAYS_TO_FETCH)
        
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        url = f"{self.BASE_URL}/{start_str}/{end_str}/"
        
        self.log(f"Fetching gold prices from {start_str} to {end_str}")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                self.log("[WARN] No data returned from NBP API")
                return []
            
            # Convert to our format and sort by date (newest first)
            prices = []
            for entry in data:
                prices.append({
                    'date': entry['data'],         # NBP uses 'data' key for date
                    'price': float(entry['cena'])  # 'cena' is the price in PLN
                })
            
            # Sort by date descending (newest first)
            prices.sort(key=lambda x: x['date'], reverse=True)
            
            self.log(f"[OK] Retrieved {len(prices)} daily prices")
            return prices
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch data from NBP API: {e}", file=sys.stderr)
            return []
    
    def get_most_recent_price(self, daily_prices: List[Dict]) -> Optional[Dict]:
        """
        Extract the most recent price from daily prices list.
        
        Args:
            daily_prices: List of price dicts sorted by date (newest first)
            
        Returns:
            Dict with 'date' and 'price' keys for most recent entry, or None
        """
        if not daily_prices:
            return None
        
        # Already sorted by date descending, so first entry is most recent
        most_recent = daily_prices[0]
        self.log(f"[DATA] Most recent price: {most_recent['date']} = {most_recent['price']} PLN/g")
        return most_recent
    
    def save_json(self, data, filepath: Path, pretty: bool = True):
        """
        Save data to JSON file.
        
        Args:
            data: Data to save (dict or list)
            filepath: Output file path
            pretty: Whether to pretty-print JSON
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2 if pretty else None, ensure_ascii=False)
        
        self.log(f"[SAVE] Saved data to {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch last 30 days of gold prices from NBP API and save to JSON files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch last 30 days and save (default locations)
  python fetch_nbp_gold_price_today.py

  # Fetch with custom output paths
  python fetch_nbp_gold_price_today.py --output-daily daily.json --output-today today.json

  # Verbose output
  python fetch_nbp_gold_price_today.py --verbose
        """
    )
    
    parser.add_argument(
        '--output-daily',
        type=Path,
        default=Path(__file__).parent.parent / 'data' / 'nbp-gold-prices-daily.json',
        help='Output JSON file for 30-day history (default: ../data/nbp-gold-prices-daily.json)'
    )
    parser.add_argument(
        '--output-today',
        type=Path,
        default=Path(__file__).parent.parent / 'data' / 'pricetoday.json',
        help='Output JSON file for most recent price (default: ../data/pricetoday.json)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print(f"NBP Daily Gold Price Fetcher (Last 30 Days)")
    print(f"{'=' * 50}")
    
    fetcher = NBPTodayGoldPriceFetcher(verbose=args.verbose)
    
    try:
        # Fetch last 30 days of prices
        daily_prices = fetcher.fetch_last_30_days()
        
        if not daily_prices:
            print("[ABORT] Failed to retrieve gold prices from NBP API", file=sys.stderr)
            return 1
        
        # Extract most recent price
        most_recent = fetcher.get_most_recent_price(daily_prices)
        
        if not most_recent:
            print("[ABORT] No recent price found in fetched data", file=sys.stderr)
            return 1
        
        print(f"\n[DATA] Price Data Summary:")
        print(f"{'=' * 50}")
        print(f"Total days retrieved: {len(daily_prices)}")
        print(f"Date range: {daily_prices[-1]['date']} to {daily_prices[0]['date']}")
        print(f"Most recent price: {most_recent['date']} = {most_recent['price']} PLN/g")
        
        # Save both files
        fetcher.save_json(daily_prices, args.output_daily)
        fetcher.save_json(most_recent, args.output_today)
        
        print(f"\n[FILES] Output Files:")
        print(f"  Daily (30 days): {args.output_daily.resolve()}")
        print(f"  Today (latest):  {args.output_today.resolve()}")
        print(f"\n[DONE] Successfully fetched and saved gold price data!")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
