# 📊 Gold Price Visualization - PLN Edition

Interactive visualization of historical gold prices in Polish Zloty (PLN) with comparisons to other assets like real estate and cars.

**Live Demo:** [wzlocie.pl](https://wzlocie.pl)  
**Author:** GitchalWoo

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

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GitchalWoo/goldpricespln.git
   cd GoldPrice
   ```

2. **Start a local server:**
   ```bash
   # Using Python 3
   python -m http.server 8000
   
   # Or using Node.js http-server
   npx http-server -p 8000
   ```

3. **Open in browser:**
   ```
   http://localhost:8000
   ```

> **Note:** To update data from official sources, see [scripts/README.md](scripts/README.md) for data fetching setup.

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
  - **Data Years:** 2013-2025 based on catalog prices for base models (Trendline/Life trim)
  - **Sources:** Autokult articles, moto.infor.pl, VW Polska official price lists, online car dealers (chceauto.pl)
  - **Methodology:** Some years were interpolated or estimated based on inflation rates due to missing official data
  - **Note:** Prices represent suggested retail prices and may vary by region, equipment options, and market promotions

---

## 🔄 Updating Data

All data downloading and updating scripts are located in the **`scripts/`** folder. This includes automated fetchers for gold prices, real estate, and wage data from official sources (NBP, Eurostat).

For complete documentation on running data scripts, setup instructions, and automation options, see **[`scripts/README.md`](scripts/README.md)**.

Quick start:
- **Windows:** `cd scripts && setup_data.bat`
- **macOS/Linux:** `cd scripts && bash setup_data.sh`

For manual updates, individual scripts, troubleshooting, and GitHub Actions setup, refer to the [scripts documentation](scripts/README.md).

---

##  Known Limitations

- **Historical Data:** NBP API only has gold prices from 2013-01-02 onwards
  - Years before 2013 are not available from the official NBP source
  - Warsaw M² and VW Golf data also starts from 2013 for consistency
- **Update Frequency:** NBP updates prices on business days only (M-F)
  - Weekend/holiday data uses last available price
- **Monthly Granularity:** Optional - default format is yearly for backward compatibility
- **Rate Limiting:** NBP API doesn't have strict rate limits but respects reasonable usage
- **VW Golf Prices:** Catalog prices for base models only
  - Some years interpolated or estimated due to incomplete historical data
  - Actual market prices may differ based on equipment, promotions, and region

---

## 🔐 Data Privacy

- No personal data is collected
- All data processing happens in the browser
- No backend API or database
- No third-party trackers

---

**Last Updated:** October 19, 2025  
**Data Current As Of:** October 19, 2025

