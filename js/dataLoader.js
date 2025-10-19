/**
 * dataLoader.js
 * Handles loading and parsing data from JSON files
 */

const DataLoader = {
    /**
     * Load JSON data from a file
     * @param {string} filePath - Path to the JSON file
     * @returns {Promise<Object>} - Parsed JSON data
     */
    async loadJSON(filePath) {
        try {
            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error(`Failed to load ${filePath}: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error loading data from ${filePath}:`, error);
            return null;
        }
    },

    /**
     * Load all data files
     * @returns {Promise<Object>} - All data organized by category
     */
    async loadAllData() {
        const [goldData, goldMonthlyData, warsawData, golfData] = await Promise.all([
            this.loadJSON('data/nbp-gold-prices.json'),
            this.loadJSON('data/nbp-gold-prices-monthly.json'),
            this.loadJSON('data/warsaw-m2-prices.json'),
            this.loadJSON('data/vw-golf-prices.json')
        ]);

        return {
            gold: goldData || [],
            goldMonthly: goldMonthlyData || [],
            warsaw: warsawData || [],
            golf: golfData || []
        };
    },

    /**
     * Find the last update date from all data
     * @param {Object} allData - All loaded data
     * @returns {string} - Formatted date string
     */
    getLastUpdateDate(allData) {
        const dates = [];
        
        if (allData.gold?.length > 0) {
            dates.push(new Date(allData.gold[allData.gold.length - 1].date));
        }
        if (allData.warsaw?.length > 0) {
            dates.push(new Date(allData.warsaw[allData.warsaw.length - 1].date));
        }
        if (allData.golf?.length > 0) {
            dates.push(new Date(allData.golf[allData.golf.length - 1].date));
        }

        if (dates.length === 0) return 'N/A';

        const latestDate = new Date(Math.max(...dates));
        return latestDate.toLocaleDateString('pl-PL');
    },

    /**
     * Format price to PLN string
     * @param {number} value - Price value
     * @returns {string} - Formatted price
     */
    formatPLN(value) {
        return new Intl.NumberFormat('pl-PL', {
            style: 'currency',
            currency: 'PLN'
        }).format(value);
    },

    /**
     * Format grams with 2 decimal places
     * @param {number} grams - Amount in grams
     * @returns {string} - Formatted grams
     */
    formatGrams(grams) {
        return new Intl.NumberFormat('pl-PL', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(grams) + ' g';
    }
};
