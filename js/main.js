/**
 * main.js
 * Entry point - Initializes the application
 */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Initializing Gold Price Visualization...');

    // Load all data
    const allData = await DataLoader.loadAllData();

    // Check if data loaded successfully
    if (!allData.gold.length || !allData.warsaw.length || !allData.golf.length) {
        console.error('❌ Failed to load all required data files');
        showError();
        return;
    }

    console.log('✅ Data loaded successfully');

    // Create charts
    ChartManager.createGoldPriceChart(allData.gold);
    ChartManager.createWarsawChart(allData.warsaw, allData.gold);
    ChartManager.createGolfChart(allData.golf, allData.gold);

    // Update last update date
    const lastUpdated = DataLoader.getLastUpdateDate(allData);
    document.getElementById('lastUpdated').textContent = lastUpdated;

    console.log('✅ Application initialized successfully');
});

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
                <li>data/warsaw-m2-prices.json</li>
                <li>data/vw-golf-prices.json</li>
            </ul>
        </div>
    `;
    mainContent.innerHTML = errorHTML;
}
