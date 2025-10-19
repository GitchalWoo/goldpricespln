/**
 * charts.js
 * Handles chart creation and updates using Chart.js
 */

// Global Chart.js configuration
Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";
Chart.defaults.color = '#6b7280';

// ============ HELPER FUNCTIONS ============

/**
 * Get tooltip callback for PLN values
 * @param {string} prefix - Optional prefix for the label
 * @returns {Function} - Tooltip callback
 */
function getTooltipPLNCallback(prefix = 'Cena: ') {
    return function(context) {
        return prefix + DataLoader.formatPLN(context.parsed.y);
    };
}

/**
 * Get tooltip callback for Gold values
 * @param {string} prefix - Optional prefix for the label
 * @returns {Function} - Tooltip callback
 */
function getTooltipGoldCallback(prefix = 'Złoto: ') {
    return function(context) {
        return prefix + context.parsed.y.toFixed(2) + 'g';
    };
}

/**
 * Get scale tick callback for PLN values
 * @returns {Function} - Tick callback
 */
function getTickPLNCallback() {
    return function(value) {
        return DataLoader.formatPLN(value);
    };
}

/**
 * Get scale tick callback for Gold values
 * @returns {Function} - Tick callback
 */
function getTickGoldCallback() {
    return function(value) {
        return value.toFixed(2) + 'g';
    };
}

/**
 * Get colors for a chart type (PLN or Gold)
 * @param {string} period - 'pln' or 'gold'
 * @param {string} colorPLN - Color for PLN mode
 * @param {string} colorGold - Color for Gold mode (optional, defaults to gold)
 * @returns {Object} - Object with borderColor and backgroundColor
 */
function getChartColors(period, colorPLN, colorGold = '#f59e0b') {
    const color = period === 'pln' ? colorPLN : colorGold;
    const bgColor = period === 'pln' ? colorPLN : colorGold;
    const opacity = 0.1;
    
    return {
        borderColor: color,
        backgroundColor: `rgba(${hexToRgb(color).join(', ')}, ${opacity})`,
        pointBackgroundColor: color
    };
}

/**
 * Convert hex color to RGB
 * @param {string} hex - Hex color code
 * @returns {Array} - [r, g, b] values
 */
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ] : [0, 0, 0];
}

const ChartManager = {
    chartInstances: {},

    /**
     * Create the gold price chart
     * @param {Array} data - Gold price data
     */
    createGoldPriceChart(data) {
        const ctx = document.getElementById('chartGold');
        if (!ctx) return;

        const chartData = {
            labels: data.map(item => item.year),
            datasets: [{
                label: 'Cena złota (PLN/g)',
                data: data.map(item => item.price),
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#f59e0b',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }]
        };

        this.chartInstances.gold = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: { size: 14 },
                        bodyFont: { size: 13 },
                        callbacks: {
                            label: getTooltipPLNCallback()
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'PLN/gram'
                        },
                        ticks: {
                            callback: getTickPLNCallback()
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Rok'
                        }
                    }
                }
            }
        });

        this.updateGoldStats(data);
    },

    /**
     * Update the gold price chart with different data
     * @param {Array} data - Gold price data (yearly or monthly)
     * @param {string} period - 'yearly' or 'monthly'
     */
    updateGoldChart(data, period) {
        const chart = this.chartInstances.gold;
        if (!chart) return;

        let labels, priceData, xTitle;

        if (period === 'yearly') {
            labels = data.map(item => item.year);
            priceData = data.map(item => item.price);
            xTitle = 'Rok';
        } else {
            // Format monthly data as "Year-Month" for better readability
            labels = data.map(item => `${item.year}-${String(item.month).padStart(2, '0')}`);
            priceData = data.map(item => item.price);
            xTitle = 'Miesiąc';
        }

        // Update chart data
        chart.data.labels = labels;
        chart.data.datasets[0].data = priceData;

        // Update x-axis title
        if (chart.options.scales && chart.options.scales.x) {
            chart.options.scales.x.title.text = xTitle;
        }

        chart.update();
        this.updateGoldStats(data);
    },

    /**
     * Create the Warsaw M² vs Gold chart (using monthly data)
     * @param {Array} warsawMonthlyData - Warsaw monthly real estate data
     */
    createWarsawChart(warsawMonthlyData) {
        const ctx = document.getElementById('chartWarsawM2');
        if (!ctx) return;

        // Filter data from 2013 onwards (before 2013, gold prices are null)
        const filteredData = warsawMonthlyData.filter(item => item.year >= 2013);

        // Default: show PLN prices
        const chartData = {
            labels: filteredData.map(item => `${item.year}-${String(item.month).padStart(2, '0')}`),
            datasets: [{
                label: 'Cena m² (PLN)',
                data: filteredData.map(item => item.priceM2_pln),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 2,
                pointBackgroundColor: '#3b82f6',
                pointHoverRadius: 5
            }]
        };

        this.chartInstances.warsaw = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: getTooltipPLNCallback()
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'PLN/m²'
                        },
                        ticks: {
                            callback: getTickPLNCallback()
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Miesiąc'
                        }
                    }
                }
            }
        });

        // Store filtered data for switcher
        this.chartInstances.warsawData = filteredData;
        this.updateWarsawStats(filteredData, 'pln');
    },

    /**
     * Update Warsaw chart to show PLN or Gold prices
     * @param {string} period - 'pln' or 'gold'
     */
    updateWarsawChartPeriod(period) {
        const chart = this.chartInstances.warsaw;
        const data = this.chartInstances.warsawData;

        if (!chart || !data) return;

        const isPLN = period === 'pln';
        const chartLabel = isPLN ? 'Cena m² (PLN)' : 'Równowartość w złocie (gramy)';
        const yAxisTitle = isPLN ? 'PLN/m²' : 'Gramy złota';
        const colors = getChartColors(period, '#3b82f6', '#f59e0b');

        // Update chart data and options
        chart.data.datasets[0].data = data.map(item => isPLN ? item.priceM2_pln : item.priceM2_gold);
        chart.data.datasets[0].label = chartLabel;
        chart.data.datasets[0].borderColor = colors.borderColor;
        chart.data.datasets[0].backgroundColor = colors.backgroundColor;
        chart.data.datasets[0].pointBackgroundColor = colors.pointBackgroundColor;

        chart.options.scales.y.title.text = yAxisTitle;
        chart.options.scales.y.ticks.callback = isPLN ? getTickPLNCallback() : getTickGoldCallback();
        chart.options.plugins.tooltip.callbacks.label = isPLN 
            ? getTooltipPLNCallback()
            : getTooltipGoldCallback();

        chart.update();
        this.updateWarsawStats(data, period);
    },

    /**
     * Create the VW Golf price chart
     * @param {Array} golfData - VW Golf price data
     * @param {Array} goldData - Gold price data
     */
    createGolfChart(golfData, goldData) {
        const ctx = document.getElementById('chartVWGolf');
        if (!ctx) return;

        // Calculate gold equivalents
        const golfWithGold = golfData.map(item => {
            const goldPrice = goldData.find(g => g.year === item.year);
            const goldEquivalent = goldPrice ? item.pricePLN / goldPrice.price : item.pricePLN;
            return {
                year: item.year,
                pricePLN: item.pricePLN,
                priceGold: goldEquivalent
            };
        });

        const chartData = {
            labels: golfWithGold.map(item => item.year),
            datasets: [{
                label: 'Cena Golfa w złocie (gramy)',
                data: golfWithGold.map(item => item.priceGold),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }]
        };

        this.chartInstances.golf = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: getTooltipGoldCallback('Złoto: ')
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Gramy złota'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(0) + 'g';
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Rok'
                        }
                    }
                }
            }
        });

        this.updateGolfStats(golfWithGold);
    },

    /**
     * Create the Minimum Wages chart
     * @param {Array} wagesData - Minimum wages yearly data
     * @param {Array} goldData - Gold price data
     */
    createMinWagesChart(wagesData, goldData) {
        const ctx = document.getElementById('chartMinWages');
        if (!ctx) return;

        // Calculate gold equivalents for wages
        const wagesWithGold = wagesData.map(item => {
            const goldPrice = goldData.find(g => g.year === item.year);
            // Gold equivalent = wage / price per gram
            const goldEquivalent = goldPrice ? item.wage / goldPrice.price : item.wage;
            return {
                year: item.year,
                wagePLN: item.wage,
                wageGold: goldEquivalent
            };
        });

        // Default: show PLN wages
        const chartData = {
            labels: wagesWithGold.map(item => item.year),
            datasets: [{
                label: 'Płaca minimalna (PLN)',
                data: wagesWithGold.map(item => item.wagePLN),
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#8b5cf6',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }]
        };

        this.chartInstances.wages = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: getTooltipPLNCallback('Płaca: ')
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'PLN'
                        },
                        ticks: {
                            callback: getTickPLNCallback()
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Rok'
                        }
                    }
                }
            }
        });

        // Store data for switcher
        this.chartInstances.wagesData = wagesWithGold;
        this.updateMinWagesStats(wagesWithGold, 'pln');
    },

    /**
     * Generic function to update wage-type charts (min wages or avg wages)
     * @param {string} chartKey - Key in chartInstances (e.g., 'wages', 'avgwages')
     * @param {string} dataKey - Key in chartInstances for data (e.g., 'wagesData', 'avgwagesData')
     * @param {string} statsUpdater - Function name to update stats (e.g., 'updateMinWagesStats', 'updateAvgWagesStats')
     * @param {Object} config - Configuration object with labels and colors
     * @param {string} period - 'pln' or 'gold'
     */
    updateWageChartPeriod(chartKey, dataKey, statsUpdater, config, period) {
        const chart = this.chartInstances[chartKey];
        const data = this.chartInstances[dataKey];

        if (!chart || !data) return;

        const isPLN = period === 'pln';
        const chartLabel = isPLN ? config.labelPLN : config.labelGold;
        const yAxisTitle = isPLN ? 'PLN' : 'Gramy złota';
        const colors = getChartColors(period, config.colorPLN, '#f59e0b');

        // Update chart data and options
        chart.data.datasets[0].data = data.map(item => isPLN ? item.wagePLN : item.wageGold);
        chart.data.datasets[0].label = chartLabel;
        chart.data.datasets[0].borderColor = colors.borderColor;
        chart.data.datasets[0].backgroundColor = colors.backgroundColor;
        chart.data.datasets[0].pointBackgroundColor = colors.pointBackgroundColor;

        chart.options.scales.y.title.text = yAxisTitle;
        chart.options.scales.y.ticks.callback = isPLN ? getTickPLNCallback() : getTickGoldCallback();
        chart.options.plugins.tooltip.callbacks.label = isPLN 
            ? getTooltipPLNCallback('Płaca: ')
            : getTooltipGoldCallback();

        chart.update();
        this[statsUpdater](data, period);
    },

    /**
     * Update Minimum Wages chart to show PLN or Gold
     * @param {string} period - 'pln' or 'gold'
     */
    updateMinWagesChartPeriod(period) {
        this.updateWageChartPeriod('wages', 'wagesData', 'updateMinWagesStats', {
            labelPLN: 'Płaca minimalna (PLN)',
            labelGold: 'Płaca minimalna w złocie (gramy)',
            colorPLN: '#8b5cf6'
        }, period);
    },

    /**
     * Update gold price statistics
     */
    updateGoldStats(data) {
        const prices = data.map(item => item.price);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;

        document.getElementById('goldMin').textContent = DataLoader.formatPLN(minPrice);
        document.getElementById('goldMax').textContent = DataLoader.formatPLN(maxPrice);
        document.getElementById('goldAvg').textContent = DataLoader.formatPLN(avgPrice);
    },

    /**
     * Update Warsaw statistics
     * @param {Array} data - Warsaw data with monthly entries
     * @param {string} period - 'pln' or 'gold' (parameter kept for compatibility but not used)
     */
    updateWarsawStats(data, period) {
        const currentData = data[data.length - 1];
        
        // Always show PLN in first stat and Gold in second stat (don't swap)
        document.getElementById('warsawM2Current').textContent = DataLoader.formatPLN(currentData.priceM2_pln);
        document.getElementById('warsawM2Gold').textContent = DataLoader.formatGrams(currentData.priceM2_gold);
    },

    /**
     * Update Golf statistics
     */
    updateGolfStats(data) {
        const oldGolf = data[0];
        const newGolf = data[data.length - 1];
        const change = ((newGolf.priceGold - oldGolf.priceGold) / oldGolf.priceGold * 100).toFixed(1);

        document.getElementById('golfOldGrams').textContent = DataLoader.formatGrams(oldGolf.priceGold);
        document.getElementById('golfNewGrams').textContent = DataLoader.formatGrams(newGolf.priceGold);
        document.getElementById('golfChange').textContent = (change > 0 ? '+' : '') + change + '%';
    },

    /**
     * Update Minimum Wages statistics
     * @param {Array} data - Wages data with yearly entries
     * @param {string} period - 'pln' or 'gold' (parameter kept for compatibility but not used)
     */
    updateMinWagesStats(data, period) {
        const currentData = data[data.length - 1];
        const oldData = data[0];
        const change = ((currentData.wagePLN - oldData.wagePLN) / oldData.wagePLN * 100).toFixed(1);
        
        // Always show PLN in first stat and Gold in second stat (don't swap)
        document.getElementById('wagesCurrentPLN').textContent = DataLoader.formatPLN(currentData.wagePLN);
        document.getElementById('wagesCurrentGold').textContent = DataLoader.formatGrams(currentData.wageGold);
        document.getElementById('wagesChange').textContent = (change > 0 ? '+' : '') + change + '%';
    },

    /**
     * Create the Average Wages chart
     * @param {Array} avgwagesData - Average wages yearly data
     * @param {Array} goldData - Gold price data
     */
    createAvgWagesChart(avgwagesData, goldData) {
        const ctx = document.getElementById('chartAvgWages');
        if (!ctx) return;

        // Calculate gold equivalents for wages
        const avgwagesWithGold = avgwagesData.map(item => {
            const goldPrice = goldData.find(g => g.year === item.year);
            // Gold equivalent = wage / price per gram
            const goldEquivalent = goldPrice ? item.wage / goldPrice.price : item.wage;
            return {
                year: item.year,
                wagePLN: item.wage,
                wageGold: goldEquivalent
            };
        });

        // Default: show PLN wages
        const chartData = {
            labels: avgwagesWithGold.map(item => item.year),
            datasets: [{
                label: 'Średnia płaca (PLN)',
                data: avgwagesWithGold.map(item => item.wagePLN),
                borderColor: '#06b6d4',
                backgroundColor: 'rgba(6, 182, 212, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#06b6d4',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }]
        };

        this.chartInstances.avgwages = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: getTooltipPLNCallback('Płaca: ')
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'PLN'
                        },
                        ticks: {
                            callback: getTickPLNCallback()
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Rok'
                        }
                    }
                }
            }
        });

        // Store data for switcher
        this.chartInstances.avgwagesData = avgwagesWithGold;
        this.updateAvgWagesStats(avgwagesWithGold, 'pln');
    },

    /**
     * Update Average Wages chart to show PLN or Gold
     * @param {string} period - 'pln' or 'gold'
     */
    updateAvgWagesChartPeriod(period) {
        this.updateWageChartPeriod('avgwages', 'avgwagesData', 'updateAvgWagesStats', {
            labelPLN: 'Średnia płaca (PLN)',
            labelGold: 'Średnia płaca w złocie (gramy)',
            colorPLN: '#06b6d4'
        }, period);
    },

    /**
     * Update Average Wages statistics
     * @param {Array} data - Average wages data with yearly entries
     * @param {string} period - 'pln' or 'gold' (parameter kept for compatibility but not used)
     */
    updateAvgWagesStats(data, period) {
        const currentData = data[data.length - 1];
        const oldData = data[0];
        const change = ((currentData.wagePLN - oldData.wagePLN) / oldData.wagePLN * 100).toFixed(1);
        
        // Always show PLN in first stat and Gold in second stat (don't swap)
        document.getElementById('avgwagesCurrentPLN').textContent = DataLoader.formatPLN(currentData.wagePLN);
        document.getElementById('avgwagesCurrentGold').textContent = DataLoader.formatGrams(currentData.wageGold);
        document.getElementById('avgwagesChange').textContent = (change > 0 ? '+' : '') + change + '%';
    }
};
