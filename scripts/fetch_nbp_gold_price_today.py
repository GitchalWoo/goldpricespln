#!/usr/bin/env python3
"""
NBP Today's Gold Price Fetcher

This script fetches the latest gold price from the National Bank of Poland (NBP) API
and saves it to a JSON file with the current date.

NBP API: https://api.nbp.pl/api/cenyzlota/
- Gold price data available from: 2013-01-02
- Daily granularity with prices in PLN per gram (1000 proof)
- Returns the most recent available price

Usage:
    python fetch_nbp_gold_price_today.py [--output ../data/pricetoday.json]
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
import argparse
import sys


class NBPTodayGoldPriceFetcher:
    """Fetches today's (most recent) gold price from NBP API."""
    
    BASE_URL = "https://api.nbp.pl/api/cenyzlota"
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def fetch_today_price(self) -> Optional[Dict]:
        """
        Fetch the most recent gold price from NBP API.
        
        The NBP API endpoint /api/cenyzlota/ returns the latest available price.
        We try to get today first, then go backwards day by day until we find data.
        
        Returns:
            Dict with 'date' and 'price' keys, or None if fetch fails
        """
        today = datetime.now()
        
        # Try today and previous days (in case today's data isn't available yet)
        # Go back up to 7 days to find the most recent available data
        for days_back in range(7):
            check_date = today - timedelta(days=days_back)
            date_str = check_date.strftime('%Y-%m-%d')
            
            # NBP API endpoint for specific date range (single day)
            url = f"{self.BASE_URL}/{date_str}/{date_str}/"
            
            self.log(f"Attempting to fetch price for: {date_str}")
            
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if data and len(data) > 0:
                    entry = data[0]  # Get the first (and should be only) entry
                    result = {
                        'date': entry['data'],      # NBP uses 'data' key for date
                        'price': float(entry['cena'])  # 'cena' is the price in PLN
                    }
                    self.log(f"[OK] Found price for {result['date']}: {result['price']} PLN/g")
                    return result
                
            except requests.exceptions.RequestException as e:
                self.log(f"[WARN] Failed to fetch data for {date_str}: {e}")
                continue
        
        return None
    
    def save_json(self, data: Dict, filepath: Path, pretty: bool = True):
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
        
        self.log(f"[SAVE] Saved price data to {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch today\'s gold price from NBP API and save to JSON file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch today's price and save (default location)
  python fetch_nbp_gold_price_today.py

  # Fetch today's price with custom output path
  python fetch_nbp_gold_price_today.py --output custom.json

  # Verbose output
  python fetch_nbp_gold_price_today.py -v
        """
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path(__file__).parent.parent / 'data' / 'pricetoday.json',
        help='Output JSON file path (default: ../data/pricetoday.json)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print(f"NBP Today's Gold Price Fetcher")
    print(f"{'=' * 50}")
    
    fetcher = NBPTodayGoldPriceFetcher(verbose=args.verbose)
    
    try:
        # Fetch today's (most recent) price
        price_data = fetcher.fetch_today_price()
        
        if not price_data:
            print("[ABORT] Failed to retrieve gold price from NBP API", file=sys.stderr)
            return 1
        
        print(f"\nPrice Data Retrieved:")
        print(f"{'=' * 50}")
        print(f"Date: {price_data['date']}")
        print(f"Price: {price_data['price']} PLN/g")
        
        # Save to JSON
        fetcher.save_json(price_data, args.output)
        
        print(f"\nOutput: {args.output.resolve()}")
        print(f"[DONE] Successfully fetched and saved today's gold price!")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
