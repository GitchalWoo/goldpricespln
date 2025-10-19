#!/usr/bin/env python3
"""
Eurostat Average Wage Downloader

This script fetches historical average full-time adjusted salary per employee data for Poland 
from the Eurostat API (European Statistical Office) and saves the results to a JSON file 
in annual format.

Eurostat API: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/
- Dataset: nama_10_fte ("Average full-time adjusted salary per employee")
- Geographic level: Poland (PL)
- Currency: National currency (PLN)
- Data available: 2013 onwards
- Format: Annual

Usage:
    python fetch_eurostat_avg_wages.py [--start-year 2013] [--output ../data/avg-wages.json]
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import sys


def load_gold_prices(filepath: Path, verbose: bool = False) -> Dict[int, float]:
    """
    Load gold prices from existing JSON file.
    
    Args:
        filepath: Path to gold prices JSON file
        verbose: Enable verbose output
        
    Returns:
        Dictionary mapping year to gold price (PLN per gram)
    """
    try:
        if verbose:
            print(f"[INFO] Loading gold prices from {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        prices = {}
        for entry in data:
            if 'year' in entry and 'price' in entry:
                prices[entry['year']] = entry['price']
        
        if verbose:
            print(f"[INFO] Loaded {len(prices)} years of gold price data")
        return prices
    except FileNotFoundError:
        print(f"[WARNING] Gold prices file not found: {filepath}")
        return {}
    except Exception as e:
        print(f"[WARNING] Error loading gold prices: {e}")
        return {}


class EurostatAverageWageFetcher:
    """Fetches and processes average wage data from Eurostat API."""
    
    BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
    DATASET_ID = "nama_10_fte"  # Average full-time adjusted salary per employee
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Eurostat-AvgWage-Fetcher/1.0'
        })
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def fetch_wage_data(self, start_year: int = 2013, end_year: Optional[int] = None) -> List[Dict]:
        """
        Fetch average wage data from Eurostat API for Poland.
        
        Args:
            start_year: Starting year (default: 2013)
            end_year: Ending year (default: current year)
            
        Returns:
            List of dicts with 'year' and 'wage' keys
        """
        if end_year is None:
            end_year = datetime.now().year
        
        url = f"{self.BASE_URL}/{self.DATASET_ID}"
        
        # Eurostat parameters: geo=PL (Poland), unit=NAC (National currency - PLN)
        params = {
            'format': 'JSON',
            'geo': 'PL',  # Poland only
            'unit': 'NAC'  # National currency (PLN)
        }
        
        self.log(f"Fetching average wage data for Poland")
        self.log(f"URL: {url}")
        self.log(f"Parameters: {params}")
        
        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            self.log(f"API Response Status: {response.status_code}")
            
            # Process the response
            wages = self._parse_api_response(data, start_year, end_year)
            self.log(f"Retrieved {len(wages)} data points")
            
            return wages
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch data from Eurostat API: {e}", file=sys.stderr)
            return []
        except (KeyError, ValueError) as e:
            print(f"[ERROR] Failed to parse API response: {e}", file=sys.stderr)
            self.log(f"Response content: {response.text if 'response' in locals() else 'N/A'}")
            return []
    
    def _parse_api_response(self, data: Dict, start_year: int, end_year: int) -> List[Dict]:
        """
        Parse the Eurostat API response and extract annual average wage data.
        
        The API returns annual data for each year. When filtered by unit=NAC,
        the structure is simplified and the value index corresponds directly to the time index.
        
        Args:
            data: API response dictionary
            start_year: Starting year to include
            end_year: Ending year to include
            
        Returns:
            List of dicts with 'year' and 'wage' keys
        """
        wages_list = []
        
        try:
            # Extract dimensions and values
            dimensions = data.get('dimension', {})
            values = data.get('value', {})
            
            self.log(f"Dimensions: {list(dimensions.keys())}")
            self.log(f"Size structure: {data.get('size')}")
            
            # Get time index mapping
            time_dim = dimensions.get('time', {})
            time_index = time_dim.get('category', {}).get('index', {})
            
            self.log(f"Available time periods: {len(time_index)}")
            
            # Iterate through time periods and extract values
            for time_code, time_idx in time_index.items():
                # Parse time code (e.g., '2013', '2014')
                try:
                    year = int(time_code)
                except ValueError:
                    continue
                
                # Only include data in requested range
                if year < start_year or year > end_year:
                    continue
                
                # When filtered by unit=NAC, the index is directly the time index
                value = values.get(str(time_idx), None)
                
                if value is not None:
                    self.log(f"  {time_code}: {value} PLN")
                    wages_list.append({
                        'year': year,
                        'wage': round(float(value), 2)
                    })
                else:
                    self.log(f"  {time_code}: No data (index {time_idx})")
            
            return sorted(wages_list, key=lambda x: x['year'])
            
        except Exception as e:
            self.log(f"Error parsing response: {e}")
            raise ValueError(f"Failed to parse API response: {e}")
    
    def combine_with_gold_prices(self, wages: List[Dict], gold_prices: Dict[int, float]) -> List[Dict]:
        """
        Combine wage data with gold price data, calculating wage in grams of gold.
        
        Args:
            wages: List of wage dicts with 'year' and 'wage' keys (PLN)
            gold_prices: Dictionary mapping year to gold price (PLN per gram)
            
        Returns:
            List of combined dicts with 'year', 'wage', and 'price' keys
        """
        combined = []
        
        for wage_entry in wages:
            year = wage_entry['year']
            wage_pln = wage_entry['wage']
            gold_price = gold_prices.get(year, None)
            
            combined_entry = {
                'year': year,
                'wage': wage_pln
            }
            
            # Calculate how many grams of gold the wage can buy
            if gold_price is not None and gold_price > 0:
                wage_in_gold_grams = wage_pln / gold_price
                combined_entry['price'] = round(wage_in_gold_grams, 2)
            
            combined.append(combined_entry)
        
        self.log(f"Combined {len(combined)} entries with wage converted to gold grams")
        return combined
    
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
        print(f"[OK] Data saved: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch average wage data from Eurostat API and save to JSON file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Eurostat API Documentation:
  https://ec.europa.eu/eurostat/
  Dataset: nama_10_fte - Average full-time adjusted salary per employee
  Country: Poland (PL)
  Currency: National currency (PLN)

Examples:
  # Fetch all available data (from 2013 onwards)
  python fetch_eurostat_avg_wages.py

  # Fetch data starting from 2015
  python fetch_eurostat_avg_wages.py --start-year 2015

  # Specify custom year range
  python fetch_eurostat_avg_wages.py --start-year 2015 --end-year 2024

  # Verbose output
  python fetch_eurostat_avg_wages.py -v

  # Custom output file
  python fetch_eurostat_avg_wages.py --output ../data/avg-wages-custom.json
        """
    )
    
    parser.add_argument(
        '--start-year',
        type=int,
        default=2013,
        help='Starting year for data retrieval (default: 2013)'
    )
    parser.add_argument(
        '--end-year',
        type=int,
        default=None,
        help='Ending year for data retrieval (default: current year)'
    )
    parser.add_argument(
        '--gold-prices',
        type=Path,
        default=Path(__file__).parent.parent / 'data' / 'nbp-gold-prices.json',
        help='Path to gold prices JSON file (default: ../data/nbp-gold-prices.json)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path(__file__).parent.parent / 'data' / 'avg-wages.json',
        help='Output JSON file path (default: ../data/avg-wages.json)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print(f"[DATA] Eurostat Average Wage Data Downloader (Poland)")
    print(f"Dataset: nama_10_fte (Average full-time adjusted salary per employee)")
    print(f"{'=' * 70}")
    
    fetcher = EurostatAverageWageFetcher(verbose=args.verbose)
    
    try:
        # Load gold prices
        print(f"\n[FILES] Loading gold prices...")
        gold_prices = load_gold_prices(args.gold_prices, verbose=args.verbose)
        
        # Fetch wage data
        print(f"\n[MONEY] Fetching average wage data...")
        wages = fetcher.fetch_wage_data(
            start_year=args.start_year,
            end_year=args.end_year
        )
        
        if not wages:
            print("[ERROR] No data retrieved from Eurostat API", file=sys.stderr)
            return 1
        
        # Combine data
        print(f"\n[LINK] Combining data...")
        combined = fetcher.combine_with_gold_prices(wages, gold_prices)
        
        print(f"\n[GRAPH] Data Summary:")
        print(f"{'=' * 70}")
        print(f"Years: {combined[0]['year']} - {combined[-1]['year']}")
        print(f"Data points: {len(combined)}")
        print(f"Min average wage: {min(w['wage'] for w in combined):.2f} PLN")
        print(f"Max average wage: {max(w['wage'] for w in combined):.2f} PLN")
        if gold_prices:
            has_prices = [c for c in combined if 'price' in c]
            if has_prices:
                print(f"Min average wage (in gold): {min(c.get('price', 0) for c in has_prices):.2f}g")
                print(f"Max average wage (in gold): {max(c.get('price', 0) for c in has_prices):.2f}g")
        
        # Save to JSON
        fetcher.save_json(combined, args.output)
        
        print(f"\n[FILES] Output file: {args.output.resolve()}")
        print(f"[DONE] Done!")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
