/**
 * goldConverter.js
 * Handles gold price conversions and asset value comparisons
 */

const GoldConverter = {
    goldMonthlyData: [],
    goldCurrentPrice: 0,

    /**
     * Initialize the Gold Converter with data
     * @param {Array} goldMonthlyData - Monthly gold price data
     */
    init(goldMonthlyData) {
        this.goldMonthlyData = goldMonthlyData;
        
        // Get current gold price (last entry)
        if (goldMonthlyData && goldMonthlyData.length > 0) {
            this.goldCurrentPrice = goldMonthlyData[goldMonthlyData.length - 1].price;
        }

        this.setupEventListeners();
        this.populateYearOptions();
    },

    /**
     * Populate year options in the year select element
     */
    populateYearOptions() {
        const yearSelect = document.getElementById('converterYear');
        if (!yearSelect) return;

        // Get unique years from gold data
        const years = [...new Set(this.goldMonthlyData.map(item => item.year))].sort((a, b) => a - b);

        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        });
    },

    /**
     * Setup event listeners for the form
     */
    setupEventListeners() {
        const calculateBtn = document.getElementById('converterCalculate');
        if (calculateBtn) {
            calculateBtn.addEventListener('click', () => this.calculate());
        }

        // Allow Enter key to trigger calculation
        const inputs = [
            document.getElementById('converterPastValue'),
            document.getElementById('converterCurrentValue')
        ];
        inputs.forEach(input => {
            if (input) {
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.calculate();
                    }
                });
            }
        });
    },

    /**
     * Get gold price for a specific year and month
     * @param {number} year - Year
     * @param {number} month - Month (1-12)
     * @returns {number|null} - Price per gram or null if not found
     */
    getGoldPrice(year, month) {
        const entry = this.goldMonthlyData.find(item => item.year === year && item.month === month);
        return entry ? entry.price : null;
    },

    /**
     * Convert PLN to grams of gold
     * @param {number} amount - Amount in PLN
     * @param {number} pricePerGram - Gold price per gram in PLN
     * @returns {number} - Amount in grams
     */
    convertPLNToGold(amount, pricePerGram) {
        if (!pricePerGram || pricePerGram === 0) return 0;
        return amount / pricePerGram;
    },

    /**
     * Format month name
     * @param {number} month - Month number (1-12)
     * @returns {string} - Polish month name
     */
    getMonthName(month) {
        const months = [
            'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
            'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
        ];
        return months[month - 1] || '';
    },

    /**
     * Perform the calculation
     */
    calculate() {
        const year = parseInt(document.getElementById('converterYear').value);
        const month = parseInt(document.getElementById('converterMonth').value);
        const pastValue = parseFloat(document.getElementById('converterPastValue').value);
        const currentValue = parseFloat(document.getElementById('converterCurrentValue').value);

        // Validate inputs
        if (!year || !month || isNaN(pastValue) || isNaN(currentValue) || pastValue < 0 || currentValue < 0) {
            alert('Proszę wypełnić wszystkie pola prawidłowymi wartościami.');
            return;
        }

        // Get gold prices
        const goldPricePast = this.getGoldPrice(year, month);
        
        if (!goldPricePast) {
            alert(`Brak danych o cenie złota dla ${this.getMonthName(month)} ${year}. Proszę wybrać inny miesiąc/rok.`);
            return;
        }

        // Calculate gold equivalents
        const pastGold = this.convertPLNToGold(pastValue, goldPricePast);
        const currentGold = this.convertPLNToGold(currentValue, this.goldCurrentPrice);

        // Calculate difference
        const difference = currentGold - pastGold;
        const percentageChange = (difference / pastGold) * 100;

        // Display results
        this.displayResults(year, month, pastValue, pastGold, currentValue, currentGold, difference, percentageChange);
    },

    /**
     * Display the calculation results
     */
    displayResults(year, month, pastValuePLN, pastValueGold, currentValuePLN, currentValueGold, difference, percentageChange) {
        const resultsContainer = document.getElementById('converterResults');
        
        // Update past value
        document.getElementById('resultPastTime').textContent = `${this.getMonthName(month)} ${year}`;
        document.getElementById('resultPastPLN').textContent = DataLoader.formatPLN(pastValuePLN);
        document.getElementById('resultPastGold').textContent = DataLoader.formatGrams(pastValueGold);

        // Update current value
        document.getElementById('resultCurrentPLN').textContent = DataLoader.formatPLN(currentValuePLN);
        document.getElementById('resultCurrentGold').textContent = DataLoader.formatGrams(currentValueGold);

        // Update comparison
        const comparisonIndicator = document.getElementById('comparisonIndicator');
        const comparisonText = document.getElementById('comparisonText');

        let badge, emoji, status;
        
        if (Math.abs(difference) < 0.01) {
            // Same value (within 0.01g tolerance)
            badge = 'same';
            emoji = '⚖️';
            status = 'ta sama';
        } else if (difference > 0) {
            badge = 'more';
            emoji = '📈';
            status = 'więcej złota';
        } else {
            badge = 'less';
            emoji = '📉';
            status = 'mniej złota';
        }

        const badgeHTML = `
            <div class="comparison-badge ${badge}">
                <span>${emoji} ${status.toUpperCase()}</span>
                <span class="change-percentage">${Math.abs(percentageChange).toFixed(1)}%</span>
            </div>
        `;

        const changeText = difference > 0 
            ? `Aktywo jest warte o <strong>${Math.abs(difference).toFixed(2)}g</strong> więcej złota (`
            : difference < 0
            ? `Aktywo jest warte o <strong>${Math.abs(difference).toFixed(2)}g</strong> mniej złota (`
            : `Aktywo jest warte tyle samo złota (`;

        comparisonText.innerHTML = changeText + 
            (difference >= 0 ? '+' : '') + 
            `${percentageChange.toFixed(1)}%)`;
        
        comparisonIndicator.innerHTML = badgeHTML;

        // Show results
        resultsContainer.style.display = 'grid';
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
};
