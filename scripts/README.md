# 📊 Data Downloader Scripts - Complete Guide

This folder contains all Python scripts for fetching and processing data from official sources (NBP, Eurostat), plus convenient setup scripts for all platforms.

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```cmd
cd scripts
setup_data.bat
```

**macOS/Linux:**
```bash
cd scripts
bash setup_data.sh
```

These scripts will:
- ✅ Detect your system (Python/Node.js)
- ✅ Install dependencies if needed
- ✅ Run all data downloaders
- ✅ Generate updated data files

### Option 2: Manual Setup

**1. Install dependencies (one time):**
```bash
pip install -r requirements.txt
```

**2. Run individual scripts:**
```bash
# Gold prices (yearly - default)
python fetch_nbp_gold_prices.py

# Gold prices (monthly)
python fetch_nbp_gold_prices.py --monthly

# Warsaw real estate prices
python fetch_warsaw_m2_prices.py

# Minimum wages vs gold
python fetch_eurostat_min_wages.py

# Average wages vs gold
python fetch_eurostat_avg_wages.py
```

---

## 📁 Scripts Overview

### 1. **fetch_nbp_gold_prices.py** ⭐ Primary Script

Fetches historical gold prices from the National Bank of Poland (NBP) API.

**Features:**
- Downloads daily gold prices (2013-present)
- Aggregates to yearly or monthly averages
- Respects 93-day API limit automatically
- Handles errors gracefully
- Production-ready code

**Output:** `../data/nbp-gold-prices.json` (yearly) or `../data/nbp-gold-prices-monthly.json` (monthly)

**Usage:**
```bash
# Yearly averages (default)
python fetch_nbp_gold_prices.py

# Monthly granularity
python fetch_nbp_gold_prices.py --monthly

# Verbose output
python fetch_nbp_gold_prices.py -v

# Custom start year
python fetch_nbp_gold_prices.py --start-year 2020

# Custom output file
python fetch_nbp_gold_prices.py --output my_prices.json

# All options
python fetch_nbp_gold_prices.py --help
```

**Data Source:**
- API: https://api.nbp.pl/api/cenyzlota/
- Unit: PLN per gram (1000 proof)
- Frequency: Weekdays only (M-F)

**Output Format:**
```json
// Yearly (default)
[
  { "year": 2013, "price": 143.58 },
  { "year": 2024, "price": 305.21 }
]

// Monthly (with --monthly)
[
  { "year": 2025, "month": 1, "price": 467.50 },
  { "year": 2025, "month": 2, "price": 458.20 }
]
```

---

### 2. **fetch_nbp_gold_prices.js** - Node.js Alternative

Same as the Python version but written in Node.js. Use this if you prefer JavaScript or don't have Python installed.

**Installation:**
```bash
npm install axios
# or use npx (no installation needed)
npx fetch_nbp_gold_prices.js
```

**Usage:** Same command-line options as Python version

---

### 3. **fetch_warsaw_m2_prices.py** - Real Estate Data

Fetches Warsaw real estate prices from NBP quarterly data and converts to gold equivalents.

**What it does:**
1. Downloads quarterly housing price data from NBP
2. Extracts Warsaw-specific average m² prices
3. Interpolates quarterly data to monthly
4. Converts PLN/m² to gold equivalent
5. Outputs both PLN and gold values

**Output:** `../data/warsaw-m2-prices-monthly.json`

**Usage:**
```bash
# Default run
python fetch_warsaw_m2_prices.py

# Verbose output
python fetch_warsaw_m2_prices.py --verbose

# Custom output file
python fetch_warsaw_m2_prices.py --output my_warsaw.json

# All options
python fetch_warsaw_m2_prices.py --help
```

**Output Format:**
```json
[
  { "year": 2013, "month": 1, "priceM2_pln": 6002.0, "priceM2_gold": 35.87 },
  { "year": 2013, "month": 2, "priceM2_pln": 6050.0, "priceM2_gold": 36.11 }
]
```

**Dependencies:**
- Requires `nbp-gold-prices.json` for gold price conversion

---

### 4. **fetch_eurostat_min_wages.py** - Minimum Wages

Fetches Polish minimum wage data from Eurostat and calculates purchasing power in gold.

**What it does:**
1. Downloads semi-annual minimum wage data from Eurostat
2. Aggregates to annual averages
3. Loads gold prices from `nbp-gold-prices.json`
4. Calculates wage purchasing power in grams of gold
5. Outputs both nominal wage and gold equivalent

**Output:** `../data/min-wages.json`

**Usage:**
```bash
# Default run
python fetch_eurostat_min_wages.py

# Verbose output
python fetch_eurostat_min_wages.py -v

# Custom start/end years
python fetch_eurostat_min_wages.py --start-year 2015 --end-year 2023

# Custom output file
python fetch_eurostat_min_wages.py --output my_wages.json

# All options
python fetch_eurostat_min_wages.py --help
```

**Output Format:**
```json
[
  { "year": 2013, "wage": 1600.0, "price": 11.14 },
  { "year": 2014, "wage": 1680.0, "price": 13.11 }
]
```

**Key Findings:**
- Minimum wages increased **191%** (2013-2025)
- Gold purchasing power **decreased 10.4%**
- Shows wage-to-asset purchasing power erosion

**Dependencies:**
- Requires `nbp-gold-prices.json` for price conversion

---

### 5. **fetch_eurostat_avg_wages.py** - Average Wages

Fetches Polish average wage data from Eurostat and calculates purchasing power in gold.

**What it does:**
1. Downloads average wage data from Eurostat (full-time adjusted salary per employee)
2. Loads gold prices from `nbp-gold-prices.json`
3. Calculates average wage purchasing power in grams of gold
4. Outputs both nominal wage and gold equivalent

**Output:** `../data/avg-wages.json`

**Usage:**
```bash
# Default run
python fetch_eurostat_avg_wages.py

# Verbose output
python fetch_eurostat_avg_wages.py -v

# Custom start/end years
python fetch_eurostat_avg_wages.py --start-year 2015 --end-year 2022

# Custom output file
python fetch_eurostat_avg_wages.py --output my_avg_wages.json

# All options
python fetch_eurostat_avg_wages.py --help
```

**Output Format:**
```json
[
  { "year": 2013, "wage": 44310.0, "price": 308.61 },
  { "year": 2023, "wage": 81999.0, "price": 312.75 }
]
```

**Key Findings:**
- Average wages increased **85%** (2013-2023)
- Gold prices increased **83%** (2013-2023)
- Real purchasing power in hard assets remained **flat (~1.3% increase)**

**Dependencies:**
- Requires `nbp-gold-prices.json` for price conversion

---

## 🔧 Setup Scripts

### setup_data.bat (Windows)

Automated setup for Windows that:
- Auto-detects Python or Node.js
- Installs `requests` package if needed
- Runs all data fetchers in sequence
- Provides clear progress output

**Usage:**
```cmd
cd scripts
setup_data.bat
```

**What happens:**
```
📁 Checking Python installation...
✅ Python found: C:\Python39\python.exe

📦 Installing dependencies...
✅ requests package installed

🔄 Running data fetchers...
[1/5] Fetching NBP gold prices (yearly)...
✅ Generated: ../data/nbp-gold-prices.json (13 entries)

[2/5] Fetching NBP gold prices (monthly)...
✅ Generated: ../data/nbp-gold-prices-monthly.json (154 entries)

[3/5] Fetching Warsaw M² prices...
✅ Generated: ../data/warsaw-m2-prices-monthly.json

[4/5] Fetching minimum wages...
✅ Generated: ../data/min-wages.json

[5/5] Fetching average wages...
✅ Generated: ../data/avg-wages.json

✨ All data updated successfully!
```

---

### setup_data.sh (macOS/Linux)

Automated setup for Unix-like systems that:
- Auto-detects Python installation
- Installs `requests` package if needed
- Runs all data fetchers in sequence
- Provides clear progress output

**Usage:**
```bash
cd scripts
bash setup_data.sh
```

**What happens:** (Same as Windows version)

---

## 📊 Dependencies

### Python Packages

All required in `requirements.txt`:

```
requests>=2.28.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

### External APIs Used

1. **NBP API** (Gold prices)
   - Endpoint: https://api.nbp.pl/api/cenyzlota/
   - No authentication needed
   - Rate limit: 93 days per request

2. **Eurostat API** (Wage data)
   - Endpoint: https://ec.europa.eu/eurostat/api/dissemination/sdmx/
   - No authentication needed
   - No strict rate limits

3. **NBP API** (Real estate)
   - Endpoint: https://api.nbp.pl/ (housing prices)
   - Quarterly data, interpolated to monthly

---

## 🎯 Execution Order & Dependencies

**Recommended execution order:**

```
1. fetch_nbp_gold_prices.py        ← Must run first (other scripts depend on it)
   ├─ Generates: nbp-gold-prices.json
   └─ Generates: nbp-gold-prices-monthly.json

2. fetch_warsaw_m2_prices.py       ← Depends on gold prices (step 1)
   └─ Generates: warsaw-m2-prices-monthly.json

3. fetch_eurostat_min_wages.py     ← Depends on gold prices (step 1)
   └─ Generates: min-wages.json

4. fetch_eurostat_avg_wages.py     ← Depends on gold prices (step 1)
   └─ Generates: avg-wages.json
```

The setup scripts automatically run in correct order.

---

## 📝 Running Scripts Manually

### Single Script

```bash
python fetch_nbp_gold_prices.py
```

### All Scripts in Sequence

**Windows (PowerShell):**
```powershell
python fetch_nbp_gold_prices.py; `
python fetch_warsaw_m2_prices.py; `
python fetch_eurostat_min_wages.py; `
python fetch_eurostat_avg_wages.py
```

**macOS/Linux (Bash):**
```bash
python fetch_nbp_gold_prices.py && \
python fetch_warsaw_m2_prices.py && \
python fetch_eurostat_min_wages.py && \
python fetch_eurostat_avg_wages.py
```

---

## 🔄 Automated Updates

### GitHub Actions (Recommended)

Set up automatic daily/weekly updates:

1. Create `.github/workflows/update-data.yml`
2. Add workflow (see example below)
3. Push to repository
4. GitHub Actions will run automatically

**Example Workflow:**
```yaml
name: Update Data

on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 2 AM UTC
  workflow_dispatch:     # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      
      - name: Run data fetchers
        run: |
          cd scripts
          python fetch_nbp_gold_prices.py
          python fetch_warsaw_m2_prices.py
          python fetch_eurostat_min_wages.py
          python fetch_eurostat_avg_wages.py
      
      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add ../data/*.json
          git commit -m "🔄 Update data: $(date)"
          git push
```

### Windows Task Scheduler

Schedule automatic updates on Windows:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Update Gold Price Data"
4. Trigger: Daily/Weekly
5. Action: `python.exe` with argument `D:\git\GoldPrice\scripts\fetch_nbp_gold_prices.py`

### Linux Cron

Add to crontab for automatic updates:

```bash
crontab -e
```

Add line:
```
0 2 * * 0 cd /path/to/GoldPrice/scripts && python fetch_nbp_gold_prices.py && python fetch_warsaw_m2_prices.py && python fetch_eurostat_min_wages.py && python fetch_eurostat_avg_wages.py
```

This runs every Sunday at 2 AM.

---

## 🚨 Troubleshooting

### "Python not found"

**Windows:**
```cmd
python --version
```

If not found, install from https://www.python.org/downloads/

**macOS/Linux:**
```bash
python3 --version
```

### "requests module not found"

```bash
pip install requests
```

or 

```bash
pip install -r requirements.txt
```

### "API connection failed"

Check internet connection:
```bash
ping api.nbp.pl
```

Verify API is accessible:
- NBP: https://api.nbp.pl/api/cenyzlota/
- Eurostat: https://ec.europa.eu/eurostat/

### "JSON file not found"

This is likely a dependency issue. Make sure you run scripts in order:

1. Run `fetch_nbp_gold_prices.py` first
2. Then run other scripts

### "Permission denied" (macOS/Linux)

Make scripts executable:
```bash
chmod +x setup_data.sh
bash setup_data.sh
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────┐
│   NBP API Endpoint  │
│ /api/cenyzlota/     │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  fetch_nbp_gold_prices.py            │
│  (Primary - generates base data)     │
└──────────┬───────────────────────────┘
           │
      ┌────┴────┐
      ▼         ▼
   ┌──┴──┐  ┌───┴────────────────────┐
   │GOLD │  │  Eurostat API          │
   └──┬──┘  │ (Wage data)            │
      │     └────┬─────────────────┬──┘
      │          │                 │
      ▼          ▼                 ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│Warsaw M2 │ │Min Wages │ │Avg Wages     │
│Converter │ │Converter │ │Converter     │
└──────────┘ └──────────┘ └──────────────┘
      │          │                 │
      └──────────┴─────────────────┘
             │
             ▼
      ┌─────────────────┐
      │  data/*.json    │
      │  (Output files) │
      └─────────────────┘
             │
             ▼
      ┌─────────────────┐
      │   Browser App   │
      │  (Visualized)   │
      └─────────────────┘
```

---

## 📚 Related Documentation

- **`../README.md`** - Main project overview
- **`../START_HERE.md`** - Getting started guide
- **`../DATA_DOWNLOADER.md`** - Complete downloader reference
- **`../context/claude.md`** - Full project context
- **Script docstrings** - Run `python fetch_*.py --help` for detailed options

---

## ✅ Quick Checklist

Before running scripts:

- [ ] Python 3.7+ installed
- [ ] Internet connection active
- [ ] `requirements.txt` installed (`pip install -r requirements.txt`)
- [ ] Sufficient disk space (~10 MB for all data files)
- [ ] Write permissions in `../data/` folder

---

## 💡 Pro Tips

1. **First run:** Run all scripts together using setup script
2. **Regular updates:** Use GitHub Actions for automatic weekly updates
3. **Testing:** Add `-v` flag to see detailed progress
4. **Debugging:** Check `*.json` files in `../data/` folder for results
5. **Custom schedule:** Modify cron/Task Scheduler timing as needed

---

## 📞 Support

### Common Issues

| Issue | Solution |
|-------|----------|
| No data generated | Check internet, verify API accessibility |
| Old data not updating | Delete old JSON files and re-run |
| Slow performance | Normal on first run (fetching 3000+ daily prices) |
| Disk space error | Free up space, or reduce date range with `--start-year` |
| Unicode errors | Ensure UTF-8 encoding, use Python 3.7+ |

---

**Last Updated:** October 19, 2025  
**Status:** ✅ Production Ready

All scripts are tested and validated. Ready for automated deployment and regular data updates!
