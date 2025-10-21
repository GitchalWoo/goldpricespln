/**
 * main.js
 * Entry point - Initializes the application
 */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Initializing Gold Price Visualization...');

    // Load all data
    const allData = await DataLoader.loadAllData();

    // Check if data loaded successfully
    if (!allData.gold.length || !allData.warsawMonthly.length || !allData.golf.length) {
        console.error('❌ Failed to load all required data files');
        showError();
        return;
    }

    console.log('✅ Data loaded successfully');

    // Initialize Gold Converter
    GoldConverter.init(allData.goldMonthly);
    console.log('✅ Gold Converter initialized');

    // Create charts
    ChartManager.createGoldPriceChart(allData.gold);
    ChartManager.createWarsawChart(allData.warsawMonthly);
    ChartManager.createMinWagesChart(allData.wages, allData.gold);
    ChartManager.createAvgWagesChart(allData.avgwages, allData.gold);
    ChartManager.createGolfChart(allData.golf, allData.gold);

    // Initialize switchers
    initPeriodSwitcher('gold', updateGoldChartPeriod, allData);
    initPeriodSwitcher('warsaw', (period) => ChartManager.updateWarsawChartPeriod(period));
    initPeriodSwitcher('wages', (period) => ChartManager.updateMinWagesChartPeriod(period));
    initPeriodSwitcher('avgwages', (period) => ChartManager.updateAvgWagesChartPeriod(period));
    initPeriodSwitcher('golf', (period) => ChartManager.updateGolfChartPeriod(period));

    // Load stock data and initialize stock charts
    await initializeStockCharts();
    console.log('✅ Stock charts initialized');

    // Update last update date
    if (allData.lastUpdate) {
        document.getElementById('lastUpdated').textContent = allData.lastUpdate.readable;
    } else {
        const lastUpdated = DataLoader.getLastUpdateDate(allData);
        document.getElementById('lastUpdated').textContent = lastUpdated;
    }

    // Initialize price widget with today's gold price
    if (allData.priceToday && allData.priceToday.price) {
        updatePriceWidget(allData.priceToday);
    }

    console.log('✅ Application initialized successfully');
});

/**
 * Generic switcher initializer that handles period switching for any chart
 * @param {string} chartName - Name of the chart (e.g., 'gold', 'warsaw', 'wages')
 * @param {Function} updateCallback - Callback function to update the chart
 * @param {Object} allData - Optional: All loaded data (used for multi-period charts like gold)
 */
function initPeriodSwitcher(chartName, updateCallback, allData) {
    const switcherButtons = document.querySelectorAll(`.switcher-btn[data-chart="${chartName}"]`);
    
    switcherButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const period = e.target.getAttribute('data-period');
            
            // Update button states and ARIA attributes
            switcherButtons.forEach(btn => {
                btn.classList.remove('switcher-btn--active');
                btn.setAttribute('aria-pressed', 'false');
            });
            e.target.classList.add('switcher-btn--active');
            e.target.setAttribute('aria-pressed', 'true');
            
            // Call the appropriate update callback
            updateCallback(period, allData);
        });
    });
}

/**
 * Wrapper for gold chart period switching
 * @param {string} period - 'yearly' or 'monthly'
 * @param {Object} allData - All loaded data
 */
function updateGoldChartPeriod(period, allData) {
    if (period === 'yearly') {
        ChartManager.updateGoldChart(allData.gold, 'yearly');
    } else if (period === 'monthly') {
        ChartManager.updateGoldChart(allData.goldMonthly, 'monthly');
    }
}

/**
 * Show error message if data failed to load
 */
function showError() {
    const mainContent = document.querySelector('.main-content');
    const errorHTML = `
        <div style="text-align: center; padding: 3rem; color: #dc2626;">
            <h2>❌ Błąd ładowania danych</h2>
            <p>Nie udało się załadować plików danych. Upewnij się, że wszystkie pliki JSON znajdują się w folderze <code>data/</code>:</p>
            <ul style="text-align: left; display: inline-block; margin: 1rem 0;">
                <li>data/nbp-gold-prices.json</li>
                <li>data/nbp-gold-prices-monthly.json</li>
                <li>data/warsaw-m2-prices.json</li>
                <li>data/vw-golf-prices.json</li>
            </ul>
        </div>
    `;
    mainContent.innerHTML = errorHTML;
}

/**
 * Update price widget with today's gold price
 * @param {Object} priceData - Price data with 'price' and 'date' fields
 */
function updatePriceWidget(priceData) {
    const widget = document.getElementById('priceWidget');
    const priceValue = document.getElementById('priceWidgetValue');
    const priceDate = document.getElementById('priceWidgetDate');
    
    if (widget && priceData.price) {
        priceValue.textContent = DataLoader.formatPLN(priceData.price) + '/g';
        
        // Format date in Polish locale
        const dateObj = new Date(priceData.date);
        priceDate.textContent = `z dnia ${dateObj.toLocaleDateString('pl-PL')}`;
        
        // Show the widget
        widget.style.display = 'flex';
    }
}

/**
 * Initialize stock charts with dynamic stock selection
 */
async function initializeStockCharts() {
    // Fetch stock configuration - it's in the scripts folder
    const stockConfig = await DataLoader.loadJSON('scripts/stock-tickers-config.json');
    if (!stockConfig || !stockConfig.stocks) {
        console.warn('⚠️ Stock configuration not found or invalid');
        console.warn('Attempted path: scripts/stock-tickers-config.json');
        return;
    }

    // Load all stock data
    const stockDataMap = await DataLoader.loadAllStocks(stockConfig.stocks);
    if (Object.keys(stockDataMap).length === 0) {
        console.warn('⚠️ No stock data loaded');
        return;
    }

    // Store stock config and data globally for switchers
    window.stockConfig = stockConfig;
    window.stockDataMap = stockDataMap;

    // Get the first available stock (default)
    const firstStock = stockConfig.stocks.find(s => stockDataMap[s.ticker]);
    if (!firstStock) {
        console.warn('⚠️ No valid stock data found');
        return;
    }

    // Create buttons for stock selection
    createStockButtons(stockConfig.stocks, stockDataMap, firstStock);

    // Create the initial chart with the first stock (default to PLN)
    ChartManager.createStockChart(stockDataMap[firstStock.ticker], 'pln');

    // Initialize period switcher for stocks
    initPeriodSwitcher('stocks', (period) => ChartManager.updateStockChartPeriod(period));

    // Add event listeners for stock selection buttons
    initStockSelectionButtons(stockDataMap);
}

/**
 * Create stock selection buttons dynamically
 * @param {Array} stocks - Array of stock config objects
 * @param {Object} stockDataMap - Map of ticker -> stock data
 * @param {Object} defaultStock - Default stock to highlight
 */
function createStockButtons(stocks, stockDataMap, defaultStock) {
    const container = document.getElementById('stockButtonsContainer');
    if (!container) return;

    container.innerHTML = ''; // Clear existing buttons

    stocks.forEach((stock) => {
        // Only create button if we have data for this stock
        if (!stockDataMap[stock.ticker]) {
            console.log(`Skipping ${stock.ticker} - no data available`);
            return;
        }

        const button = document.createElement('button');
        button.className = 'switcher-btn';
        button.setAttribute('data-ticker', stock.ticker);
        button.setAttribute('aria-label', `Wyświetl wykres ${stock.name}`);
        button.textContent = stock.name;
        
        // Mark the default stock as active
        if (stock.ticker === defaultStock.ticker) {
            button.classList.add('switcher-btn--active');
            button.setAttribute('aria-pressed', 'true');
        } else {
            button.setAttribute('aria-pressed', 'false');
        }

        container.appendChild(button);
    });
}

/**
 * Initialize click handlers for stock selection buttons
 * @param {Object} stockDataMap - Map of ticker -> stock data
 */
function initStockSelectionButtons(stockDataMap) {
    const buttons = document.querySelectorAll('#stockButtonsContainer .switcher-btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const ticker = e.target.getAttribute('data-ticker');
            const stockData = stockDataMap[ticker];

            if (!stockData) {
                console.error(`Stock data not found for ticker: ${ticker}`);
                return;
            }

            // Update active button and ARIA attributes
            buttons.forEach(btn => {
                btn.classList.remove('switcher-btn--active');
                btn.setAttribute('aria-pressed', 'false');
            });
            e.target.classList.add('switcher-btn--active');
            e.target.setAttribute('aria-pressed', 'true');

            // Get current period setting from the period switcher buttons
            const periodButtons = document.querySelectorAll('.switcher-btn[data-chart="stocks"]');
            const currentPeriod = Array.from(periodButtons)
                .find(btn => btn.classList.contains('switcher-btn--active'))
                ?.getAttribute('data-period') || 'gold';

            // Create new chart with selected stock
            ChartManager.createStockChart(stockData, currentPeriod);
        });
    });
}
