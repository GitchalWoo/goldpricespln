#!/usr/bin/env python3
"""
Unified Data Updater - Runs all data fetchers in correct dependency order

This script orchestrates all data fetching scripts with proper error handling,
logging, and a summary report. It's used by GitHub Actions but can also be
run manually for local testing.

Usage:
    python update_all_data.py [--verbose] [--skip-validation]
    
Environment Variables:
    UPDATE_DATA_VERBOSE - Set to '1' to enable verbose mode
    UPDATE_DATA_SKIP_VALIDATION - Set to '1' to skip data validation
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import os
import argparse


class DataUpdater:
    """Orchestrates data fetching and validation."""
    
    def __init__(self, verbose: bool = False, skip_validation: bool = False):
        self.verbose = verbose
        self.skip_validation = skip_validation
        self.scripts_dir = Path(__file__).parent
        self.data_dir = self.scripts_dir.parent / 'data'
        self.results: Dict[str, dict] = {}
        self.start_time = datetime.now()
    
    def log(self, message: str, level: str = 'INFO'):
        """Print log message with timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        prefix = f"[{timestamp}] {level}"
        print(f"{prefix}: {message}")
    
    def log_verbose(self, message: str):
        """Print message only in verbose mode."""
        if self.verbose:
            self.log(message, 'DEBUG')
    
    def run_script(self, script_name: str, description: str, args: List[str] = None) -> bool:
        """
        Run a data fetching script.
        
        Args:
            script_name: Name of Python script to run
            description: Human-readable description for logging
            args: Additional command-line arguments
            
        Returns:
            True if successful, False otherwise
        """
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            self.log(f"Script not found: {script_path}", 'ERROR')
            return False
        
        # Build command
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        if self.verbose:
            cmd.append('-v')
        
        self.log(f"[RUN] Running: {description}")
        self.log_verbose(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.scripts_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per script
            )
            
            if result.stdout and self.verbose:
                self.log_verbose(f"Output:\n{result.stdout}")
            
            if result.returncode != 0:
                self.log(
                    f"Script failed with exit code {result.returncode}",
                    'ERROR'
                )
                if result.stderr:
                    self.log(f"Error output:\n{result.stderr}", 'ERROR')
                return False
            
            self.log(f"[OK] {description} completed successfully", 'SUCCESS')
            return True
            
        except subprocess.TimeoutExpired:
            self.log(f"Script timeout after 5 minutes: {script_name}", 'ERROR')
            return False
        except Exception as e:
            self.log(f"Failed to run script: {e}", 'ERROR')
            return False
    
    def validate_data_file(self, filename: str, expected_keys: Optional[List[str]] = None) -> bool:
        """
        Validate that a data file exists and contains valid JSON.
        
        Args:
            filename: Name of JSON file in data directory
            expected_keys: Optional list of keys to check in each entry
            
        Returns:
            True if valid, False otherwise
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            self.log(f"Data file not found: {filename}", 'WARN')
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list) or len(data) == 0:
                self.log(f"Data file empty or invalid format: {filename}", 'WARN')
                return False
            
            # Check expected keys if provided
            if expected_keys:
                first_entry = data[0]
                missing_keys = [k for k in expected_keys if k not in first_entry]
                if missing_keys:
                    self.log(
                        f"Data file missing expected keys: {missing_keys} in {filename}",
                        'WARN'
                    )
                    return False
            
            self.log(f"[OK] Validated {filename}: {len(data)} entries")
            return True
            
        except json.JSONDecodeError as e:
            self.log(f"Invalid JSON in {filename}: {e}", 'ERROR')
            return False
        except Exception as e:
            self.log(f"Error validating {filename}: {e}", 'ERROR')
            return False
    
    def update_all_data(self) -> bool:
        """
        Execute all data fetchers in dependency order.
        
        Order matters because later scripts depend on gold prices being available.
        
        Returns:
            True if all scripts succeeded, False otherwise
        """
        self.log("=" * 60)
        self.log("[DATA] Starting Automated Data Update", 'INFO')
        self.log("=" * 60)
        self.log(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        self.log(f"Verbose mode: {'enabled' if self.verbose else 'disabled'}")
        self.log(f"Data directory: {self.data_dir}")
        self.log("")
        
        # Step 1: Gold prices (PRIMARY - others depend on this)
        self.log("[STEP-1] STEP 1: Fetch Gold Prices (Primary)")
        self.log("-" * 40)
        
        success = True
        
        # Yearly gold prices
        if not self.run_script(
            'fetch_nbp_gold_prices.py',
            'NBP Gold Prices (Yearly)',
            ['--output', str(self.data_dir / 'nbp-gold-prices.json')]
        ):
            self.log("[FAIL] Failed to fetch yearly gold prices", 'WARN')
            success = False
        
        if not self.skip_validation:
            self.validate_data_file(
                'nbp-gold-prices.json',
                expected_keys=['year', 'price']
            )
        
        # Monthly gold prices
        if not self.run_script(
            'fetch_nbp_gold_prices.py',
            'NBP Gold Prices (Monthly)',
            ['--monthly', '--output', str(self.data_dir / 'nbp-gold-prices-monthly.json')]
        ):
            self.log("[FAIL] Failed to fetch monthly gold prices", 'WARN')
            success = False
        
        if not self.skip_validation:
            self.validate_data_file(
                'nbp-gold-prices-monthly.json',
                expected_keys=['year', 'month', 'price']
            )
        
        self.log("")
        
        if not success:
            self.log("[ABORT] Primary data (gold prices) failed - aborting remaining scripts", 'ERROR')
            return False
        
        # Step 2: Secondary data (depends on gold prices)
        self.log("[STEP-2] STEP 2: Fetch Secondary Data (Depends on Gold Prices)")
        self.log("-" * 40)
        
        all_secondary_success = True
        
        # Warsaw m2 prices
        if not self.run_script(
            'fetch_warsaw_m2_prices.py',
            'Warsaw m2 Real Estate Prices'
        ):
            all_secondary_success = False
        
        if not self.skip_validation:
            self.validate_data_file(
                'warsaw-m2-prices-monthly.json',
                expected_keys=['year', 'month', 'priceM2_pln']
            )
        
        # Minimum wages
        if not self.run_script(
            'fetch_eurostat_min_wages.py',
            'Minimum Wages Data'
        ):
            all_secondary_success = False
        
        if not self.skip_validation:
            self.validate_data_file(
                'min-wages.json',
                expected_keys=['year', 'wage', 'price']
            )
        
        # Average wages
        if not self.run_script(
            'fetch_eurostat_avg_wages.py',
            'Average Wages Data'
        ):
            all_secondary_success = False
        
        if not self.skip_validation:
            self.validate_data_file(
                'avg-wages.json',
                expected_keys=['year', 'wage', 'price']
            )
        
        # Stock prices
        if not self.run_script(
            'fetch_stock_prices.py',
            'Stock Prices (Yahoo Finance)'
        ):
            all_secondary_success = False
        
        self.log("")
        
        # Step 3: Update timestamp
        self.log("[STEP-3] STEP 3: Update Timestamp")
        self.log("-" * 40)
        
        if not self.run_script(
            'update_timestamp.py',
            'Update Last Modified Timestamp'
        ):
            self.log("[WARN] Failed to update timestamp", 'WARN')
            all_secondary_success = False
        
        self.log("")
        
        # Summary
        self.log("=" * 60)
        if all_secondary_success and success:
            self.log("[OK] ALL DATA UPDATED SUCCESSFULLY!", 'SUCCESS')
        else:
            self.log("[WARN] Some data fetchers failed (see details above)", 'WARN')
        
        elapsed_time = datetime.now() - self.start_time
        self.log(f"Elapsed time: {elapsed_time.total_seconds():.1f} seconds")
        self.log("=" * 60)
        
        return all_secondary_success and success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Update all data files from official sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Standard update
  python update_all_data.py
  
  # Verbose mode
  python update_all_data.py --verbose
  
  # Skip validation (faster)
  python update_all_data.py --skip-validation
  
  # Both
  python update_all_data.py -v --skip-validation
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=os.environ.get('UPDATE_DATA_VERBOSE') == '1',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        default=os.environ.get('UPDATE_DATA_SKIP_VALIDATION') == '1',
        help='Skip data file validation after fetch'
    )
    
    args = parser.parse_args()
    
    updater = DataUpdater(
        verbose=args.verbose,
        skip_validation=args.skip_validation
    )
    
    try:
        success = updater.update_all_data()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[ABORT] Update interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
