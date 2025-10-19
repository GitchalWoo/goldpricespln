# 📥 Data Downloader Guide

## Overview

This project includes a Python data downloader script that fetches real gold price data from the **NBP (Narodowy Bank Polski)** API and transforms it into JSON format for use in the visualization.

- ✅ **Python Version:** `scripts/fetch_nbp_gold_prices.py`

---

## 📊 What the Scripts Do

1. **Fetch Daily Data:** Retrieves daily gold prices from NBP API (2013-present)
2. **Smart Chunking:** Respects NBP's 93-day limit by fetching in chunks
3. **Aggregate:** Combines daily prices into monthly or yearly averages
4. **Validate:** Sorts data chronologically and validates prices
5. **Export:** Saves formatted JSON to `data/nbp-gold-prices.json`

### Data Source
- **NBP API:** https://api.nbp.pl/api/cenyzlota/
- **Available From:** 2013-01-02 onwards
- **Update Frequency:** Daily (weekdays only - M-F)
- **Unit:** PLN per gram (1000 proof)

---

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)

**On macOS/Linux:**
```bash
bash setup_data.sh
```

**On Windows:**
```cmd
setup_data.bat
```

This script automatically installs dependencies and fetches the data.

### Option 2: Manual Setup

#### Using Python 3

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Fetch and update data
python scripts/fetch_nbp_gold_prices.py
```

---

## 🎛️ Command-Line Options

### Python Version

```bash
python scripts/fetch_nbp_gold_prices.py [OPTIONS]

Options:
  --start-year YEAR     Starting year for data (default: 2013)
  --output FILE         Output JSON file path (default: data/nbp-gold-prices.json)
  --monthly             Save monthly data instead of yearly
  -v, --verbose         Show detailed progress output
  -h, --help            Show this help message
```

**Examples:**

```bash
# Fetch all data, yearly average, verbose output
python scripts/fetch_nbp_gold_prices.py -v

# Fetch data from 2020 onwards
python scripts/fetch_nbp_gold_prices.py --start-year 2020

# Save monthly granularity data
python scripts/fetch_nbp_gold_prices.py --monthly --output data/nbp-gold-prices-monthly.json

# Custom output location
python scripts/fetch_nbp_gold_prices.py --output /path/to/prices.json
```

---

## 📋 Output Format

### Yearly Average (Default)

```json
[
  { "year": 2013, "price": 143.58 },
  { "year": 2014, "price": 128.11 },
  { "year": 2015, "price": 140.58 },
  ...
]
```

### Monthly Detail (with `--monthly`)

```json
[
  { "year": 2013, "month": 1, "price": 167.32 },
  { "year": 2013, "month": 2, "price": 163.47 },
  { "year": 2013, "month": 3, "price": 163.95 },
  ...
]
```

---

## 🔄 Automated Updates

### GitHub Actions (Recommended for Production)

Create `.github/workflows/update-data.yml`:

```yaml
name: Update Gold Price Data

on:
  schedule:
    # Run every Sunday at 2 AM UTC
    - cron: '0 2 * * 0'
  workflow_dispatch:

jobs:
  update-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      
      - name: Fetch gold price data
        run: python scripts/fetch_nbp_gold_prices.py
      
      - name: Commit and push
        run: |
          git config user.name "Data Bot"
          git config user.email "bot@example.com"
          git add data/nbp-gold-prices.json
          git commit -m "Update gold price data" --allow-empty
          git push
```

### Local Cron Job (macOS/Linux)

```bash
# Edit crontab
crontab -e

# Add this line to run update every Sunday at 2 AM
0 2 * * 0 cd /path/to/GoldPrice && python scripts/fetch_nbp_gold_prices.py
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Weekly, Sundays, 2 AM
4. Set action: Run program
5. Program: `python.exe`
6. Arguments: `scripts/fetch_nbp_gold_prices.py`
7. Start in: `/path/to/GoldPrice`

---

## 🧪 Testing the Script

### Verify Installation

```bash
# Test Python
python -c "import requests; print('✓ requests module available')"

# Test Node.js
node -e "console.log('✓ Node.js ready')"
```

### Test with Limited Data

```bash
# Fetch only last 6 months of data (faster)
python scripts/fetch_nbp_gold_prices.py --start-year 2025

# Fetch data with verbose output to see progress
python scripts/fetch_nbp_gold_prices.py -v
```

### Validate Output

```bash
# Check if JSON is valid
python -m json.tool data/nbp-gold-prices.json > /dev/null && echo "✓ Valid JSON"

# Count entries
python -c "import json; data = json.load(open('data/nbp-gold-prices.json')); print(f'✓ {len(data)} entries')"
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"

**Solution:**
```bash
pip install requests
# or
pip install -r scripts/requirements.txt
```

### "Connection refused" or "Cannot reach api.nbp.pl"

**Possible causes:**
- Internet connection issue
- NBP API is down (check https://api.nbp.pl/)
- Corporate firewall blocking access

**Solution:**
- Check internet connection
- Wait a moment and retry
- Verify NBP API is accessible in your browser
- Try from a different network

### "HTTP 400: Przekroczony limit"

This means the date range exceeds the 93-day limit. The script should handle this automatically, but if you see this error:

**Solution:**
- The script handles this internally, so this shouldn't occur
- If it does, report an issue on GitHub
- Try running with `--start-year` closer to present date

### JSON file not being created

**Possible causes:**
- Permission issue in data/ folder
- Script encountered an error and exited
- Output path is incorrect

**Solution:**
```bash
# Check folder permissions
ls -la data/

# Run with verbose output to see errors
python scripts/fetch_nbp_gold_prices.py -v

# Ensure data folder exists
mkdir -p data/
```

### "OSError: [Errno 2] No such file or directory"

**Solution:**
```bash
# Create scripts and data directories
mkdir -p scripts data
```

---

## 📈 Data Limits

- **Time Range:** 2013-01-02 to present (daily data)
- **Minimum Fetch:** 1 day
- **Maximum Fetch Per Request:** 93 days (API limit)
- **Daily Prices:** Only weekdays (Monday-Friday)

The script handles all of this automatically by:
1. Breaking large requests into 93-day chunks
2. Fetching sequentially to avoid hitting rate limits
3. Sorting and validating all prices

---

## 💡 Advanced Usage

### Combining Multiple Data Sources

```bash
# Fetch historical data (2013+) from NBP
python scripts/fetch_nbp_gold_prices.py --output data/nbp-historical.json

# Manually add pre-2013 data if available
# Edit data/nbp-gold-prices.json to prepend older prices
```

### Exporting to CSV

```python
import json
import csv

with open('data/nbp-gold-prices.json') as f:
    data = json.load(f)

with open('data/nbp-gold-prices.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
```

### Calculating Price Changes

```bash
python -c "
import json

with open('data/nbp-gold-prices.json') as f:
    data = json.load(f)

first = data[0]['price']
last = data[-1]['price']
change = ((last - first) / first) * 100

print(f'Price change: {change:.1f}%')
print(f'{data[0]['year']}: {first} PLN/g')
print(f'{data[-1]['year']}: {last} PLN/g')
"
```

---

## 📚 References

- [NBP Web API Documentation](https://api.nbp.pl/)
- [NBP API Examples](https://api.nbp.pl/static/dotnetapiclient.html)
- [Python requests Library](https://requests.readthedocs.io/)
- [Node.js https Module](https://nodejs.org/api/https.html)

---

## ✅ Checklist for Data Updates

- [ ] Run the downloader script
- [ ] Verify output JSON file was created
- [ ] Check JSON is valid (no syntax errors)
- [ ] Open visualization to confirm charts updated
- [ ] Commit changes to git
- [ ] Push to remote repository
- [ ] Check GitHub Pages deployed the update

---

**Last Updated:** October 19, 2025
