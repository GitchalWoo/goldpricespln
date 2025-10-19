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
     * Create the Warsaw M² vs Gold chart
     * @param {Array} warsawData - Warsaw real estate data
     * @param {Array} goldData - Gold price data
     */
    createWarsawChart(warsawData, goldData) {
        const ctx = document.getElementById('chartWarsawM2');
        if (!ctx) return;

        // Calculate gold equivalents
        const warsawWithGold = warsawData.map(item => {
            const goldPrice = goldData.find(g => g.year === item.year);
            const goldEquivalent = goldPrice ? item.priceM2 / goldPrice.price : item.priceM2;
            return {
                year: item.year,
                pricePLN: item.priceM2,
                priceGold: goldEquivalent
            };
        });

        const chartData = {
            labels: warsawWithGold.map(item => item.year),
            datasets: [
                {
                    label: 'Cena m² (PLN)',
                    data: warsawWithGold.map(item => item.pricePLN),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y',
                    pointRadius: 3,
                    pointBackgroundColor: '#3b82f6'
                },
                {
                    label: 'Równowartość w złocie (gramy)',
                    data: warsawWithGold.map(item => item.priceGold),
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.05)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y1',
                    pointRadius: 3,
                    pointBackgroundColor: '#f59e0b'
                }
            ]
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
                        padding: 12
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        position: 'left',
                        title: {
                            display: true,
                            text: 'PLN'
                        },
                        ticks: {
                            callback: function(value) {
                                return DataLoader.formatPLN(value);
                            }
                        }
                    },
                    y1: {
                        type: 'linear',
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Gramy złota'
                        },
                        grid: {
                            drawOnChartArea: false
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

        this.updateWarsawStats(warsawWithGold);
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
     */
    updateWarsawStats(data) {
        const currentData = data[data.length - 1];
        
        document.getElementById('warsawM2Current').textContent = DataLoader.formatPLN(currentData.pricePLN);
        document.getElementById('warsawM2Gold').textContent = DataLoader.formatGrams(currentData.priceGold);
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
