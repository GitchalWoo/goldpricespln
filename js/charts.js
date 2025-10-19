/**
 * charts.js
 * Handles chart creation and updates using Chart.js
 */

// Global Chart.js configuration
Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";
Chart.defaults.color = '#6b7280';

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
                            label: function(context) {
                                return 'Cena: ' + DataLoader.formatPLN(context.parsed.y);
                            }
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
                            callback: function(value) {
                                return DataLoader.formatPLN(value);
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
                            label: function(context) {
                                return 'Cena: ' + DataLoader.formatPLN(context.parsed.y);
                            }
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
                            callback: function(value) {
                                return DataLoader.formatPLN(value);
                            }
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

        let chartLabel, tooltipFormat;

        if (period === 'pln') {
            chartLabel = 'Cena m² (PLN)';
            chart.data.datasets[0].data = data.map(item => item.priceM2_pln);
            chart.options.scales.y.title.text = 'PLN/m²';
            chart.options.scales.y.ticks.callback = function(value) {
                return DataLoader.formatPLN(value);
            };
            tooltipFormat = 'pln';
        } else {
            chartLabel = 'Równowartość w złocie (gramy)';
            chart.data.datasets[0].data = data.map(item => item.priceM2_gold);
            chart.options.scales.y.title.text = 'Gramy złota';
            chart.options.scales.y.ticks.callback = function(value) {
                return value.toFixed(2) + 'g';
            };
            tooltipFormat = 'gold';
        }

        chart.data.datasets[0].label = chartLabel;
        chart.data.datasets[0].borderColor = period === 'pln' ? '#3b82f6' : '#f59e0b';
        chart.data.datasets[0].backgroundColor = period === 'pln' ? 'rgba(59, 130, 246, 0.1)' : 'rgba(245, 158, 11, 0.1)';
        chart.data.datasets[0].pointBackgroundColor = period === 'pln' ? '#3b82f6' : '#f59e0b';

        // Update tooltip format
        if (period === 'pln') {
            chart.options.plugins.tooltip.callbacks.label = function(context) {
                return 'Cena: ' + DataLoader.formatPLN(context.parsed.y);
            };
        } else {
            chart.options.plugins.tooltip.callbacks.label = function(context) {
                return 'Złoto: ' + context.parsed.y.toFixed(2) + 'g';
            };
        }

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
                            label: function(context) {
                                return 'Złoto: ' + DataLoader.formatGrams(context.parsed.y);
                            }
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
     * @param {string} period - 'pln' or 'gold'
     */
    updateWarsawStats(data, period) {
        const currentData = data[data.length - 1];
        
        if (period === 'pln') {
            document.getElementById('warsawM2Current').textContent = DataLoader.formatPLN(currentData.priceM2_pln);
            document.getElementById('warsawM2Gold').textContent = DataLoader.formatGrams(currentData.priceM2_gold);
        } else {
            document.getElementById('warsawM2Current').textContent = DataLoader.formatGrams(currentData.priceM2_gold);
            document.getElementById('warsawM2Gold').textContent = DataLoader.formatPLN(currentData.priceM2_pln);
        }
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
    }
};
