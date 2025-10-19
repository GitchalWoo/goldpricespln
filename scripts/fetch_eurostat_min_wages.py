#!/usr/bin/env python3
"""
Eurostat Minimum Wage Downloader

This script fetches historical minimum wage data for Poland from the Eurostat API
(European Statistical Office) and saves the results to a JSON file in annual format.

Eurostat API: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/
- Dataset: earn_mw_cur (Monthly minimum wages - bi-annual data        print(f"\n📈 Data Summary:")
        print(f"{'=' * 70}")
        print(f"Years: {combined[0]['year']} - {combined[-1]['year']}")
        print(f"Data points: {len(combined)}")
        print(f"Min wage: {min(w['wage'] for w in combined):.2f} PLN")
        print(f"Max wage: {max(w['wage'] for w in combined):.2f} PLN")
        if gold_prices:
            has_prices = [c for c in combined if 'price' in c]
            if has_prices:
                print(f"Min wage (in gold grams): {min(c.get('price', 0) for c in has_prices):.2f}g")
                print(f"Max wage (in gold grams): {max(c.get('price', 0) for c in has_prices):.2f}g")phic level: Poland (PL)
- Currency: National currency (PLN)
- Data available: 1999 onwards
- Format: Aggregated from semi-annual (S1, S2) to annual averages

Usage:
    python fetch_gus_wages.py [--start-year 2013] [--output ../data/min-wages.json]
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


class EurostatMinimumWageFetcher:
    """Fetches and processes minimum wage data from Eurostat API."""
    
    BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
    DATASET_ID = "earn_mw_cur"  # Monthly minimum wages - bi-annual data
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Eurostat-MinWage-Fetcher/1.0'
        })
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def fetch_wage_data(self, start_year: int = 2013, end_year: Optional[int] = None) -> List[Dict]:
        """
        Fetch minimum wage data from Eurostat API for Poland and aggregate to annual values.
        
        Args:
            start_year: Starting year (default: 2013)
            end_year: Ending year (default: current year)
            
        Returns:
            List of dicts with 'year' and 'wage' keys (annual averages)
        """
        if end_year is None:
            end_year = datetime.now().year
        
        url = f"{self.BASE_URL}/{self.DATASET_ID}"
        
        # Eurostat parameters: geo=PL (Poland), currency=NAC (National currency - PLN)
        params = {
            'format': 'JSON',
            'geo': 'PL'  # Poland only
        }
        
        self.log(f"Fetching minimum wage data for Poland")
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
        Parse the Eurostat API response and extract annual minimum wage data.
        
        The API returns semi-annual data (S1, S2) for each year in a flat indexed structure.
        We need to:
        1. Map indices back to time periods using dimension information
        2. Filter by year range
        3. Aggregate semi-annual values to annual average
        4. Filter for National Currency (NAC) values
        
        Args:
            data: API response dictionary
            start_year: Starting year to include
            end_year: Ending year to include
            
        Returns:
            List of dicts with 'year' and 'wage' keys
        """
        wages_dict = {}
        
        try:
            # Extract dimensions and values
            dimensions = data.get('dimension', {})
            id_list = data.get('id', [])  # ['freq', 'currency', 'geo', 'time']
            size_list = data.get('size', [])  # [1, 3, 1, 54]
            values = data.get('value', {})
            
            self.log(f"Dimensions: {list(dimensions.keys())}")
            self.log(f"ID structure: {id_list}")
            self.log(f"Size structure: {size_list}")
            
            # Get time index mapping
            time_dim = dimensions.get('time', {})
            time_index = time_dim.get('category', {}).get('index', {})
            time_label = time_dim.get('category', {}).get('label', {})
            
            self.log(f"Available time periods: {len(time_index)}")
            
            # Get currency index mapping
            currency_dim = dimensions.get('currency', {})
            currency_index = currency_dim.get('category', {}).get('index', {})
            
            # NAC = National currency (PLN for Poland)
            nac_idx = currency_index.get('NAC', None)
            self.log(f"NAC (National currency) index: {nac_idx}")
            
            if nac_idx is None:
                raise ValueError("NAC (National currency) not found in currency dimension")
            
            # Calculate strides for multi-dimensional indexing
            # id_list = ['freq', 'currency', 'geo', 'time']
            # size_list = [1, 3, 1, 54]
            stride_freq = size_list[1] * size_list[2] * size_list[3]  # 3*1*54 = 162
            stride_currency = size_list[2] * size_list[3]  # 1*54 = 54
            stride_geo = size_list[3]  # 54
            stride_time = 1
            
            self.log(f"Index strides - freq: {stride_freq}, currency: {stride_currency}, geo: {stride_geo}, time: {stride_time}")
            
            # Iterate through time periods and extract values for NAC currency
            for time_code, time_idx in time_index.items():
                # Parse time code (e.g., '2013-S1', '2013-S2')
                if '-' not in time_code:
                    continue
                
                year_str, semester_str = time_code.split('-')
                try:
                    year = int(year_str)
                except ValueError:
                    continue
                
                # Only include data in requested range
                if year < start_year or year > end_year:
                    continue
                
                # Calculate the index for this specific data point
                # freq_idx=0, currency_idx=nac_idx, geo_idx=0, time_idx
                flat_index = (0 * stride_freq + 
                            nac_idx * stride_currency + 
                            0 * stride_geo + 
                            time_idx * stride_time)
                
                value = values.get(str(flat_index), None)
                
                if value is not None:
                    self.log(f"  {time_code}: {value} PLN")
                    
                    if year not in wages_dict:
                        wages_dict[year] = []
                    wages_dict[year].append(float(value))
                else:
                    self.log(f"  {time_code}: No data (index {flat_index})")
            
            # Aggregate semi-annual values to annual averages
            annual_wages = []
            for year in sorted(wages_dict.keys()):
                values_list = wages_dict[year]
                if values_list:
                    avg_wage = sum(values_list) / len(values_list)
                    annual_wages.append({
                        'year': year,
                        'wage': round(avg_wage, 2)
                    })
                    self.log(f"Annual average for {year}: {round(avg_wage, 2)} PLN")
            
            return annual_wages
            
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
            List of combined dicts with 'year', 'wage', and 'wage_in_gold_grams' keys
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
        print(f"✅ Data saved: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch minimum wage data from Eurostat API and save to JSON file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Eurostat API Documentation:
  https://ec.europa.eu/eurostat/
  Dataset: earn_mw_cur - Monthly minimum wages (bi-annual data)
  Country: Poland (PL)
  Currency: National currency (PLN)

Examples:
  # Fetch all available data (from 2013 onwards)
  python fetch_gus_wages.py

  # Fetch data starting from 2015
  python fetch_gus_wages.py --start-year 2015

  # Specify custom year range
  python fetch_gus_wages.py --start-year 2015 --end-year 2024

  # Verbose output
  python fetch_gus_wages.py -v

  # Custom output file
  python fetch_gus_wages.py --output ../data/min-wages-custom.json
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
        default=Path(__file__).parent.parent / 'data' / 'min-wages.json',
        help='Output JSON file path (default: ../data/min-wages.json)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print(f"📊 Eurostat Minimum Wage Data Downloader (Poland)")
    print(f"Dataset: earn_mw_cur (Monthly minimum wages - bi-annual data)")
    print(f"{'=' * 70}")
    
    fetcher = EurostatMinimumWageFetcher(verbose=args.verbose)
    
    try:
        # Load gold prices
        print(f"\n📁 Loading gold prices...")
        gold_prices = load_gold_prices(args.gold_prices, verbose=args.verbose)
        
        # Fetch wage data
        print(f"\n💰 Fetching wage data...")
        wages = fetcher.fetch_wage_data(
            start_year=args.start_year,
            end_year=args.end_year
        )
        
        if not wages:
            print("[ERROR] No data retrieved from Eurostat API", file=sys.stderr)
            return 1
        
        # Combine data
        print(f"\n� Combining data...")
        combined = fetcher.combine_with_gold_prices(wages, gold_prices)
        
        print(f"\n�📈 Data Summary:")
        print(f"{'=' * 70}")
        print(f"Years: {combined[0]['year']} - {combined[-1]['year']}")
        print(f"Data points: {len(combined)}")
        print(f"Min wage: {min(w['wage'] for w in combined):.2f} PLN")
        print(f"Max wage: {max(w['wage'] for w in combined):.2f} PLN")
        if gold_prices:
            has_prices = [c for c in combined if 'price' in c]
            if has_prices:
                print(f"Min gold price: {min(c.get('price', 0) for c in has_prices):.2f} PLN/g")
                print(f"Max gold price: {max(c.get('price', 0) for c in has_prices):.2f} PLN/g")
        
        # Save to JSON
        fetcher.save_json(combined, args.output)
        
        print(f"\n📁 Output file: {args.output.resolve()}")
        print(f"✨ Done!")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
