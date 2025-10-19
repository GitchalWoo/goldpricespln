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
- **Options to evaluate:**
  - Chart.js (lightweight, easy to use)
  - Plotly.js (interactive, feature-rich)
  - D3.js (powerful, steeper learning curve)
  - Recharts or Visx (React-based alternatives)
- **Decision:** TBD based on simplicity and interactivity needs

### Data Format
- **Primary Format:** JSON (easier to work with in JS)
- **Alternative:** CSV (can be parsed or converted to JSON)
- **Storage:** Local files in the repo (no API calls)

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
2. ⏳ Research NBP data format and access method
3. ⏳ Set up basic HTML structure with sections for 3 graphs
4. ⏳ Choose and configure charting library
5. ⏳ Gather/create sample data files
6. ⏳ Implement data loading logic
7. ⏳ Build Graph 1 (Gold prices)
8. ⏳ Build Graph 2 (Warsaw M² vs Gold)
9. ⏳ Build Graph 3 (VW Golf in Gold)
10. ⏳ Polish UI/UX and Polish language implementation
11. ⏳ Deploy to GitHub Pages
12. ⏳ Test across devices and browsers

---

## Key Decisions to Make

- [ ] Chart library selection
- [ ] Data file format (JSON vs CSV)
- [ ] Real estate data source
- [ ] Car pricing data source
- [ ] Color scheme and design aesthetic
- [ ] Mobile-first vs desktop-first approach

---

## Resources & References

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
**Status:** Project Setup Phase
