# Gold Price Visualization Project - Context

## Project Overview
A static HTML page showcasing gold prices in PLN (Polish Zloty) with interactive visualizations. The site will be hosted on GitHub Pages with no backend API—all data processing and rendering happens in the browser.

**Language:** Polish  
**Target Audience:** Polish speakers interested in gold price trends and asset comparisons  
**Hosting:** GitHub Pages  

---

## MVP Specifications

### Core Features
Three interactive scrollable graphs showing:

1. **Graph 1: Gold Price in PLN (2000-Present)**
   - Historical gold prices from year 2000
   - Y-axis: PLN/gram
   - X-axis: Years
   - Show long-term trend

2. **Graph 2: Warsaw M² Price vs Gold Price**
   - Average m² price in Warsaw in PLN
   - Converted to grams of gold equivalent
   - Side-by-side or overlay comparison
   - Show value correlation over time

3. **Graph 3: Volkswagen Golf Price in Gold**
   - Historical VW Golf price (new model)
   - Converted to grams of gold
   - Show how much gold needed to buy a Golf through time
   - Interesting perspective on price inflation

### Future Enhancements
- Bitcoin comparisons
- Other assets (real estate, cars, commodities)
- Additional Polish cities' real estate data
- Year-over-year growth rates

---

## Data Sources

### Primary: NBP (Narodowy Bank Polski)
- **URL:** https://nbp.pl/statystyka-i-sprawozdawczosc/kursy/
- **Data Format:** JSON or CSV (to be determined)
- **Update Frequency:** Monitor NBP's data availability
- **Note:** NBP provides gold price in grams (consistent with project needs)

### Secondary Data (To Research/Gather)
- **Warsaw M² Prices:** Historical real estate data (possible sources: GUS, real estate portals)
- **VW Golf Prices:** Historical MSRP or local pricing data

---

## Technical Stack

### Frontend Framework
- **Selected:** Chart.js v4.4.0 from CDN ✅
  - Lightweight and responsive
  - Perfect for business analytics
  - Easy dual-axis chart (for Graph 2)
  - Great tooltip and legend customization
  - No build step required

### Data Format
- **Primary Format:** JSON ✅ **SELECTED**
- **Storage:** Local files in the `data/` folder
- **Update Method:** Manual JSON file updates or scripted imports from NBP

### HTML/CSS
- Semantic HTML5
- Modern CSS (Flexbox/Grid for layout)
- Responsive design for mobile viewing
- Dark/light mode consideration

### Additional Libraries
- Date parsing: `date-fns` or native Date API
- Data transformation: Utility functions (keep lightweight)

---

## Project Structure

```
GoldPrice/
├── index.html              # Main page
├── css/
│   └── style.css           # Main stylesheet
├── js/
│   ├── main.js             # Entry point, initialization
│   ├── charts.js           # Chart rendering logic
│   └── dataLoader.js       # Data loading and transformation
├── data/
│   ├── nbp-gold-prices.json       # Gold prices (2000-present)
│   ├── warsaw-m2-prices.json      # Warsaw real estate data
│   └── vw-golf-prices.json        # VW Golf price data
├── .gitignore
├── README.md               # Project documentation
└── LICENSE                 # Open source license

```

---

## Development Guidelines

### Code Style
- Modern ES6+ JavaScript (no build step needed)
- Clear, descriptive variable names in English (code) & Polish (UI strings)
- Comments in English for clarity
- Modular functions (data loading, chart creation, transformations)

### Performance Considerations
- Single-page load with lazy rendering if needed
- Smooth animations (CSS transitions)
- Debounce scroll events for interactivity
- Keep data files under 1MB each

### Accessibility
- Semantic HTML
- Sufficient color contrast
- Alt text for charts/images
- Keyboard navigation support
- ARIA labels where appropriate

### Polish Language Implementation
- All UI text in Polish
- Date formatting in Polish locale
- Currency symbol: zł (PLN)
- Decimal separator: comma (,) or period (.) per Polish standard

---

## Git Workflow

- **Repository Name:** `GoldPrice`
- **GitHub Pages Branch:** `main` (or `gh-pages` subdirectory)
- **Commit Messages:** English, clear and descriptive
- **.gitignore:** Include node_modules, IDE files, OS files

---

## Next Steps

1. ✅ Create project structure and `claude.md` (THIS FILE)
2. ✅ Set up basic HTML structure with sections for 3 graphs
3. ✅ Choose and configure charting library (Chart.js selected)
4. ✅ Implement data loading logic
5. ✅ Create sample data files with structures
6. ✅ Build Graph 1 (Gold prices)
7. ✅ Build Graph 2 (Warsaw M² vs Gold - dual axis)
8. ✅ Build Graph 3 (VW Golf in Gold)
9. ⏳ Research real NBP data format and integrate
10. ⏳ Research real Warsaw real estate data sources
11. ⏳ Research real VW Golf pricing data
12. ⏳ Replace sample data with real data
13. ⏳ Polish UI/UX refinements and testing
14. ⏳ Deploy to GitHub Pages
15. ⏳ Test across devices and browsers

---

## Key Decisions to Make

- [x] Chart library selection → **Chart.js selected**
- [x] Data file format → **JSON selected**
- [ ] Real estate data source (GUS, real estate portals, etc.)
- [ ] Car pricing data source (historical MSRP, local pricing)
- [x] Color scheme and design aesthetic → **Gold/Amber primary color with clean modern design**
- [x] Mobile-first vs desktop-first approach → **Responsive design supporting both**

---

## Implementation Notes

### HTML (`index.html`)
- Semantic structure with `<header>`, `<main>`, `<section>`, `<footer>`
- Sticky navigation bar for easy section jumping
- 3 main graph sections with descriptions
- Statistics cards below each chart
- Info section with attribution and disclaimer

### CSS (`css/style.css`)
- CSS Custom Properties (variables) for maintainability
- Flexbox and CSS Grid for layout
- Responsive breakpoints: 1200px (desktop), 768px (tablet), 480px (mobile)
- Gold color scheme (#f59e0b) as primary brand color
- Smooth animations and transitions
- Dark mode ready (structure in place)

### JavaScript Architecture
- **`dataLoader.js`** - Handles JSON fetching, formatting, and locale support
  - `loadJSON()` - Fetch individual files
  - `loadAllData()` - Promise.all() for parallel loading
  - `formatPLN()`, `formatGrams()` - Polish locale formatting
  
- **`charts.js`** - Chart.js wrapper and chart creation
  - `createGoldPriceChart()` - Simple line chart
  - `createWarsawChart()` - Dual-axis line chart (PLN vs grams)
  - `createGolfChart()` - Simple line chart
  - `updateStats()` methods - Populate stat cards
  
- **`main.js`** - Application entry point
  - Waits for DOM load
  - Orchestrates data loading and chart creation
  - Error handling with user-friendly messages

### Polish Language Features
- All UI text in Polish (headers, labels, tooltips)
- `toLocaleDateString('pl-PL')` for date formatting
- `Intl.NumberFormat('pl-PL')` for currency and number formatting
- Polish decimal separator support (comma or period)

---

## Project Status

### ✅ Completed (Skeleton Phase)
- Project structure (folders: css/, js/, data/)
- HTML5 semantic structure with 3 graph sections
- Responsive CSS with grid layout and animations
- Chart.js integration with Chart.js v4.4.0
- Data loading module (async JSON fetching)
- Chart rendering module (3 interactive charts)
- Main initialization script
- Sample data files (25-year sample data 2000-2024)
- Navigation bar with smooth scrolling
- Statistics display boxes under each chart
- Mobile-responsive design

### 📊 Charts Implemented
1. **Gold Price Chart** - Line chart with historical prices (2000-2024)
2. **Warsaw M² vs Gold** - Dual-axis comparison (PLN vs grams)
3. **VW Golf in Gold** - Line chart showing gold equivalent cost

### 🎯 Current Data Structure
- `nbp-gold-prices.json` - Year and PLN/gram price
- `warsaw-m2-prices.json` - Year and m² price in PLN
- `vw-golf-prices.json` - Year and Golf price in PLN

---

- **NBP Official Site:** https://nbp.pl/
- **GitHub Pages Setup:** https://docs.github.com/en/pages
- **Charting Libraries Comparison:** Research phase
- **Polish Locale Standards:** ISO 4217 (PLN), date format guidelines

---

## Notes

- Keep the MVP focused—avoid scope creep
- Ensure all data sources are clearly attributed
- Consider data freshness: how often to update?
- Mobile responsiveness is important (scrolling experience)
- Make it visually appealing but maintain clarity

---

**Last Updated:** 2025-10-19  
**Status:** ✅ Skeleton Complete - Ready for Real Data Integration
