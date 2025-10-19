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

    // Update last update date
    const lastUpdated = DataLoader.getLastUpdateDate(allData);
    document.getElementById('lastUpdated').textContent = lastUpdated;

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
            
            // Update button states
            switcherButtons.forEach(btn => btn.classList.remove('switcher-btn--active'));
            e.target.classList.add('switcher-btn--active');
            
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
