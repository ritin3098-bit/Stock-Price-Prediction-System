// Global variables
let stockChart = null;
let selectedAlgorithm = 'linear';
let selectedCompany = '';

// DOM Elements
const companySelect = document.getElementById('companySelect');
const daysInput = document.getElementById('daysInput');
const predictBtn = document.getElementById('predictBtn');
const algorithmButtons = document.querySelectorAll('.btn-algorithm');
const loadingSpinner = document.getElementById('loadingSpinner');
const companyInfo = document.getElementById('companyInfo');
const statsCard = document.getElementById('statsCard');

// Initialize Chart
const ctx = document.getElementById('stockChart').getContext('2d');

// Event Listeners
companySelect.addEventListener('change', handleCompanyChange);
predictBtn.addEventListener('click', handlePredict);

algorithmButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        algorithmButtons.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        selectedAlgorithm = this.getAttribute('data-algo');
    });
});

// Handle company selection
async function handleCompanyChange() {
    selectedCompany = companySelect.value;
    
    if (selectedCompany) {
        predictBtn.disabled = false;
        await loadCompanyInfo(selectedCompany);
    } else {
        predictBtn.disabled = true;
        companyInfo.style.display = 'none';
    }
}

// Load company information
async function loadCompanyInfo(symbol) {
    try {
        const response = await fetch(`/company/info/?symbol=${symbol}`);
        
        // Check if response is OK
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Check for error in response data
        if (data.error) {
            console.error('API Error:', data.error);
            alert(`Error: ${data.error}`);
            return;
        }
        
        // Validate that we have the required data
        if (!data.name || data.current_price === undefined) {
            console.error('Incomplete data received:', data);
            alert('Incomplete company information received. Please try another company.');
            return;
        }
        
        // Update company header
        document.getElementById('companyName').textContent = data.name || symbol;
        document.getElementById('companySymbol').textContent = data.symbol || symbol;
        
        // Update company info with safe defaults
        document.getElementById('currentPrice').textContent = `${(data.current_price || 0).toFixed(2)}`;
        
        const netChange = data.net_change || 0;
        const netChangeEl = document.getElementById('netChange');
        netChangeEl.textContent = `${netChange >= 0 ? '+' : ''}${netChange.toFixed(2)}`;
        netChangeEl.style.color = netChange >= 0 ? '#4caf50' : '#ff6b6b';
        
        const percentChange = data.percent_change || 0;
        const percentChangeEl = document.getElementById('percentChange');
        percentChangeEl.textContent = `${percentChange >= 0 ? '+' : ''}${percentChange.toFixed(2)}%`;
        percentChangeEl.style.color = percentChange >= 0 ? '#4caf50' : '#ff6b6b';
        
        // Update volume (check if it exists and is not null)
        const volumeEl = document.getElementById('volume');
        if (data.volume !== null && data.volume !== undefined) {
            volumeEl.textContent = data.volume.toLocaleString();
        } else {
            volumeEl.textContent = 'N/A';
        }
        
        // Show company info card
        companyInfo.style.display = 'block';
        
        // Add animation
        companyInfo.style.animation = 'none';
        setTimeout(() => {
            companyInfo.style.animation = 'fadeIn 0.5s ease-out';
        }, 10);
        
        console.log('Company info loaded successfully:', symbol);
        
    } catch (error) {
        console.error('Error loading company info:', error);
        console.error('Failed for symbol:', symbol);
        alert('Could not load company information. Please try again.');
        companyInfo.style.display = 'none';
    }
}

// Handle prediction
async function handlePredict() {
    if (!selectedCompany) {
        alert('Please select a company first!');
        return;
    }
    
    const days = parseInt(daysInput.value);
    
    if (days < 1 || days > 365) {
        alert('Please enter a valid number of days (1-365)');
        return;
    }
    
    // Show loading
    loadingSpinner.style.display = 'block';
    predictBtn.disabled = true;
    predictBtn.textContent = '⏳ Predicting...';
    
    try {
        const endpoint = selectedAlgorithm === 'linear' ? 
            '/predict/linear/' : '/predict/lstm/';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                symbol: selectedCompany,
                days: days
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Update chart
        updateChart(data);
        
        // Update statistics
        updateStatistics(data, days);
        
    } catch (error) {
        console.error('Error making prediction:', error);
        alert('An error occurred while making the prediction. Please try again.');
    } finally {
        loadingSpinner.style.display = 'none';
        predictBtn.disabled = false;
        predictBtn.textContent = '🔮 Predict Stock Price';
    }
}

// Update chart with prediction data
function updateChart(data) {
    const allDates = [...data.historical_dates, ...data.dates];
    const historicalPrices = [...data.historical_prices, ...Array(data.dates.length).fill(null)];
    const predictedPrices = [...Array(data.historical_dates.length).fill(null), ...data.predictions];
    
    // Connect historical to predicted
    predictedPrices[data.historical_dates.length - 1] = data.historical_prices[data.historical_prices.length - 1];
    
    if (stockChart) {
        stockChart.destroy();
    }
    
    stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allDates,
            datasets: [
                {
                    label: 'Historical Prices',
                    data: historicalPrices,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: `Predicted Prices (${data.algorithm})`,
                    data: predictedPrices,
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#ff6b6b',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    borderDash: [10, 5],
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += '$' + context.parsed.y.toFixed(2);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        color: '#666'
                    },
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45,
                        autoSkip: true,
                        maxTicksLimit: 10
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Price ($)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        color: '#666'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Update statistics panel
function updateStatistics(data, days) {
    const lastPredictedPrice = data.predictions[data.predictions.length - 1];
    const currentPrice = data.current_price;
    const priceChange = ((lastPredictedPrice - currentPrice) / currentPrice) * 100;
    
    document.getElementById('algoUsed').textContent = data.algorithm;
    document.getElementById('predictedPrice').textContent = `${lastPredictedPrice.toFixed(2)}`;
    document.getElementById('forecastDays').textContent = `${days} days`;
    
    const changeElement = document.getElementById('priceChange');
    const changeText = `${priceChange > 0 ? '+' : ''}${priceChange.toFixed(2)}%`;
    changeElement.textContent = changeText;
    
    // Color based on positive or negative change
    if (priceChange > 0) {
        changeElement.style.color = '#4caf50';
    } else if (priceChange < 0) {
        changeElement.style.color = '#ff6b6b';
    } else {
        changeElement.style.color = '#fff';
    }
    
    // Display accuracy
    if (data.accuracy !== undefined) {
        const accuracyEl = document.getElementById('modelAccuracy');
        accuracyEl.textContent = `${data.accuracy.toFixed(1)}%`;
        
        // Color code accuracy
        if (data.accuracy >= 80) {
            accuracyEl.style.color = '#4caf50'; // Green - Excellent
        } else if (data.accuracy >= 60) {
            accuracyEl.style.color = '#ff9800'; // Orange - Good
        } else {
            accuracyEl.style.color = '#ff6b6b'; // Red - Poor
        }
    }
    
    // Display confidence level
    if (data.confidence) {
        const confidenceEl = document.getElementById('confidenceLevel');
        confidenceEl.textContent = data.confidence;
        
        // Color code confidence
        if (data.confidence === 'High') {
            confidenceEl.style.color = '#4caf50';
        } else if (data.confidence === 'Medium') {
            confidenceEl.style.color = '#ff9800';
        } else {
            confidenceEl.style.color = '#ff6b6b';
        }
    }
    
    statsCard.style.display = 'block';
    statsCard.style.animation = 'none';
    setTimeout(() => {
        statsCard.style.animation = 'fadeIn 0.5s ease-out';
    }, 10);
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Stock Price Predictor initialized');
    
    // Add event listener for Enter key on days input
    daysInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !predictBtn.disabled) {
            handlePredict();
        }
    });
});