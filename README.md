# 📊 Gold Price Visualization - PLN Edition

Interactive visualization of historical gold prices in Polish Zloty (PLN) with comparisons to other assets like real estate and cars.

**Live Demo:** [GitHub Pages Link] (coming soon)

---

## 🎯 Features

### Gold Value Calculator
- **💰 Kalkulator Wartości w Złocie** - Compare any asset's value over time
  - Select year and month from 2013-2024
  - Enter asset value (wage, car, property, etc.) from that period
  - Enter current value and see the gold equivalent comparison
  - Automatically calculates if your asset is worth more, same, or less gold today

### Interactive Charts
Three interactive, scrollable charts showcasing:

1. **Gold Price in PLN (2013-Present)**
   - Historical gold prices from 2013 onwards (NBP data)
   - Y-axis: PLN per gram
   - X-axis: Years
   - Long-term trend visualization

2. **Warsaw M² Price vs Gold**
   - Average m² price in Warsaw in PLN
   - Converted to grams of gold equivalent
   - Side-by-side comparison
   - Shows asset correlation over time

3. **Volkswagen Golf Price in Gold**
   - Historical VW Golf price converted to grams of gold
   - Shows how much gold needed to buy a Golf through time
   - Interesting perspective on price inflation

---

## 📁 Project Structure

```
GoldPrice/
├── index.html              # Main page
├── css/
│   └── style.css           # Main stylesheet
├── js/
│   ├── main.js             # Entry point, initialization
│   ├── charts.js           # Chart rendering logic (Chart.js)
│   └── dataLoader.js       # Data loading and transformation
├── data/
│   ├── nbp-gold-prices.json           # Yearly gold prices (auto-generated)
│   ├── nbp-gold-prices-monthly.json   # Monthly gold prices (optional)
│   ├── warsaw-m2-prices.json          # Warsaw real estate data
│   └── vw-golf-prices.json            # VW Golf price data
├── scripts/
│   ├── fetch_nbp_gold_prices.py       # Python data downloader
│   └── fetch_nbp_gold_prices.js       # Node.js data downloader
├── README.md               # This file
├── claude.md               # Project context and decisions
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7+ (for Python scripts) OR Node.js 12+ (for Node.js script)
- Internet connection (to fetch NBP data)
- Python packages: `pip install -r scripts/requirements.txt` (requests, openpyxl)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GitchalWoo/goldpricespln.git
   cd GoldPrice
   ```

2. **Update gold price data (optional):**
   
   **Using Python:**
   ```bash
   python scripts/fetch_nbp_gold_prices.py
   ```
   
   **Using Node.js:**
   ```bash
   node scripts/fetch_nbp_gold_prices.js
   ```

3. **Start a local server:**
   ```bash
   # Using Python 3
   python -m http.server 8000
   
   # Or using Node.js http-server
   npx http-server -p 8000
   ```

4. **Open in browser:**
   ```
   http://localhost:8000
   ```

---

## 📊 Data Sources

### Gold Prices (NBP)
- **Source:** [Narodowy Bank Polski (NBP) Web API](https://api.nbp.pl/)
- **Endpoint:** `https://api.nbp.pl/api/cenyzlota/`
- **Data Available:** 2013-01-02 to present
- **Granularity:** Daily prices (aggregated to monthly/yearly in scripts)
- **Unit:** PLN per gram (1000 proof)
- **Update Frequency:** Daily (M-F only, bank working days)

### Other Data Sources
- **Warsaw M² Prices:** [GUS](https://stat.gov.pl/), real estate portals (manually updated)
- **VW Golf Prices:** Historical MSRP, local dealer pricing (manually updated)

---

## 🔄 Updating Data

### Automatic Gold Price Updates

The project includes a Python script to automatically fetch and update gold price data from NBP:

#### Gold Prices - Python Version

```bash
# Fetch yearly average data (default, backward compatible)
python scripts/fetch_nbp_gold_prices.py

# Fetch monthly granularity data
python scripts/fetch_nbp_gold_prices.py --monthly --output data/nbp-gold-prices-monthly.json

# Fetch data starting from a specific year
python scripts/fetch_nbp_gold_prices.py --start-year 2015

# Show verbose output
python scripts/fetch_nbp_gold_prices.py -v

# Full help
python scripts/fetch_nbp_gold_prices.py --help
```

#### Warsaw M² Prices - Python Version

Fetches quarterly Warsaw real estate prices from NBP, interpolates to monthly granularity, and converts to gold equivalent:

```bash
# Fetch Warsaw M² prices and generate monthly data with gold conversion
python scripts/fetch_warsaw_m2_prices.py

# Show verbose output
python scripts/fetch_warsaw_m2_prices.py --verbose

# Custom output file
python scripts/fetch_warsaw_m2_prices.py --output custom_output.json
```

#### Eurostat Minimum Wage + Gold Analysis - Python Version

Fetches Polish minimum wage data from Eurostat and calculates wage purchasing power in gold:

```bash
# Fetch minimum wage data and combine with gold prices
python scripts/fetch_eurostat_min_wages.py

# Show verbose output
python scripts/fetch_eurostat_min_wages.py -v

# Custom output file
python scripts/fetch_eurostat_min_wages.py --output custom_output.json

# Specific year range
python scripts/fetch_eurostat_min_wages.py --start-year 2015 --end-year 2024
```

**What it does:**
1. Downloads bi-annual minimum wage data from Eurostat API
2. Aggregates semi-annual data to annual averages
3. Loads existing gold price data from `nbp-gold-prices.json`
4. Calculates wage purchasing power in grams of gold
5. Generates `min-wages.json` with wage and gold equivalent

**Output Format:**
```json
[
  { "year": 2013, "wage": 1600.0, "price": 11.14 },
  { "year": 2014, "wage": 1680.0, "price": 13.11 }
]
```

**Key Finding:** While minimum wages increased 191% from 2013 to 2025, purchasing power in gold decreased ~10.4% due to gold price inflation.

**What it does:**
1. Downloads quarterly housing price data from NBP (Q3 2006 - present)
2. Extracts Warsaw-specific average m² prices
3. Interpolates quarterly data to monthly using linear interpolation
4. Converts monthly prices from PLN to gold equivalent using NBP gold prices
5. Generates `warsaw-m2-prices-monthly.json` with both PLN and gold values

**Output Format:**
```json
[
  { "year": 2013, "month": 1, "priceM2_pln": 6002.0, "priceM2_gold": 35.87 },
  { "year": 2013, "month": 2, "priceM2_pln": 6050.0, "priceM2_gold": 36.11 }
]
```

#### How It Works

1. **Iterative Fetching:** The script fetches data in 93-day chunks (NBP API limit)
2. **Daily Aggregation:** Downloaded daily prices are aggregated to monthly averages
3. **Yearly Fallback:** Monthly data can be further aggregated to yearly averages for backward compatibility
4. **JSON Output:** Data is saved in the appropriate JSON file with proper formatting

#### Output Formats

**Yearly Format** (default):
```json
[
  { "year": 2013, "price": 143.58 },
  { "year": 2014, "price": 128.11 }
]
```

**Monthly Format** (with `--monthly` flag):
```json
[
  { "year": 2013, "month": 1, "price": 167.32 },
  { "year": 2013, "month": 2, "price": 163.47 }
]
```

### Manual Data Updates

For Warsaw M² prices and VW Golf prices, edit the JSON files directly:

```json
[
  { "year": 2024, "price": 15000 }
]
```

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Responsive design with Flexbox/Grid
- **JavaScript (ES6+)** - No build step required
- **Chart.js v4.4.0** - Interactive charting from CDN

### Data Processing
- **Python 3** - Primary data downloader (requests library)
- **Node.js** - Alternative JavaScript-based downloader
- **NBP Web API** - Real-time gold price data

### Hosting
- **GitHub Pages** - Static site hosting
- **Git** - Version control

---

## 📖 How It Works

### Data Flow

```
NBP API
   ↓
fetch_nbp_gold_prices.py/js
   ↓
Daily prices aggregated to monthly/yearly
   ↓
JSON files in data/ folder
   ↓
Browser loads data via dataLoader.js
   ↓
Charts rendered with Chart.js
```

### JavaScript Modules

- **`dataLoader.js`** - Fetches JSON files and provides formatted data
- **`charts.js`** - Creates and manages Chart.js instances
- **`main.js`** - Orchestrates loading and rendering

---

## 🌐 Browser Compatibility

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Responsive design supports:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

---

## 📝 Configuration

### Date Formatting
Polish locale date formatting is applied automatically via `Intl.DateTimeFormat('pl-PL')`

### Currency Display
All values displayed in PLN (zł) with proper Polish number formatting

### Color Scheme
Primary color: Gold/Amber (#f59e0b)
Dark theme ready (CSS variables defined)

---

## 🚨 Known Limitations

- **Historical Data:** NBP API only has gold prices from 2013-01-02 onwards
  - Years before 2013 are not available from the official NBP source
  - Warsaw M² and VW Golf data also starts from 2013 for consistency
- **Update Frequency:** NBP updates prices on business days only (M-F)
  - Weekend/holiday data uses last available price
- **Monthly Granularity:** Optional - default format is yearly for backward compatibility
- **Rate Limiting:** NBP API doesn't have strict rate limits but respects reasonable usage

---

## 🔐 Data Privacy

- No personal data is collected
- All data processing happens in the browser
- No backend API or database
- No third-party trackers

---

## 📄 License

[Your chosen license - add appropriate license file]

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Data Contribution

To contribute updated data:
1. Verify data accuracy from official sources
2. Update appropriate JSON files in `data/` folder
3. Follow existing format and date ranges
4. Submit PR with source attribution

---

## 🐛 Troubleshooting

### Script Fails to Connect to NBP API
- Check internet connection
- Verify NBP API is accessible: https://api.nbp.pl/api/cenyzlota/
- Note: API requires HTTPS (HTTP not supported since August 1, 2025)

### JSON File Not Found
- Ensure script ran successfully without errors
- Check file permissions in `data/` folder
- Try running script with `-v` flag for detailed output

### Charts Not Displaying
- Open browser DevTools (F12) and check Console tab
- Verify JSON files are properly formatted (use JSONLint)
- Ensure Chart.js CDN is accessible

### Python Script Issues

**Module not found (requests):**
```bash
pip install requests
```

**Permission denied:**
```bash
chmod +x scripts/fetch_nbp_gold_prices.py
```

---

## 📚 Resources

- [NBP Web API Documentation](https://api.nbp.pl/)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [Polish Locale Standards](https://en.wikipedia.org/wiki/Polish_language#Writing_system)

---

## 📞 Contact & Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation in `claude.md`

---

**Last Updated:** October 19, 2025  
**Data Current As Of:** October 19, 2025

