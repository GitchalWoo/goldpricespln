#!/usr/bin/env python3
"""
Timestamp Updater - Records the last update date/time

This script creates a last-update.json file containing the current date and time
in multiple formats for use by the web application. It should be run as the last
step in the data update process.

Usage:
    python update_timestamp.py [--output-dir DATA_DIR]
    
Output:
    Creates last-update.json in the data directory with structure:
    {
        "timestamp": "2025-10-19T14:30:45",
        "date": "2025-10-19",
        "time": "14:30:45",
        "readable": "19 października 2025 o 14:30:45",
        "iso": "2025-10-19T14:30:45"
    }
"""

import json
from pathlib import Path
from datetime import datetime
import argparse
import sys


def generate_timestamp(output_dir: Path) -> bool:
    """
    Generate a last-update.json file with current timestamp.
    
    Args:
        output_dir: Directory where to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        now = datetime.now()
        
        # Create timestamp data in multiple formats
        timestamp_data = {
            "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "readable": now.strftime("%d %B %Y o %H:%M:%S"),
            "iso": now.isoformat()
        }
        
        output_file = output_dir / 'last-update.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(timestamp_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Successfully created {output_file}")
        print(f"     Timestamp: {timestamp_data['timestamp']}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error generating timestamp: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate last-update.json with current timestamp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default (saves to ../data/)
  python update_timestamp.py
  
  # Custom output directory
  python update_timestamp.py --output-dir /path/to/data
        """
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'data',
        help='Directory to save last-update.json (default: ../data/)'
    )
    
    args = parser.parse_args()
    
    try:
        success = generate_timestamp(args.output_dir)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
