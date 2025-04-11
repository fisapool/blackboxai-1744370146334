// Utility functions for formatting data
function formatTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = Math.floor(minutes % 60);
    return `${hours}h ${mins}m`;
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString();
}

// Risk level configurations
const RISK_LEVELS = {
    low: {
        color: 'green',
        icon: 'smile',
        message: 'Everything looks good!'
    },
    medium: {
        color: 'yellow',
        icon: 'meh',
        message: 'Consider taking a break soon'
    },
    high: {
        color: 'red',
        icon: 'frown',
        message: 'Time to take action!'
    }
};

// API interaction functions
async function fetchMetrics() {
    try {
        const response = await fetch('/api/current_metrics');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching metrics:', error);
        return null;
    }
}

async function fetchHistory(hours = 24) {
    try {
        const response = await fetch(`/api/history?hours=${hours}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching history:', error);
        return null;
    }
}

// UI update functions
function updateRiskIndicator(riskLevel) {
    const config = RISK_LEVELS[riskLevel] || RISK_LEVELS.low;
    const indicator = document.getElementById('riskIndicator');
    
    if (indicator) {
        // Update risk indicator styling
        indicator.className = `w-16 h-16 rounded-full flex items-center justify-center text-white bg-${config.color}-500`;
        indicator.innerHTML = `<i class="fas fa-${config.icon} text-2xl"></i>`;
        
        // Update risk text
        document.getElementById('riskLevel').textContent = 
            riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1) + ' Risk';
        document.getElementById('riskMessage').textContent = config.message;
    }
}

function updateActivityMetrics(metrics) {
    // Update basic metrics
    const elements = {
        'mouseClicks': metrics.mouse_clicks,
        'keyPresses': metrics.key_presses,
        'screenTime': formatTime(metrics.screen_time),
        'currentApp': metrics.current_app
    };

    for (const [id, value] of Object.entries(elements)) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
}

function updateRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    if (!container) return;

    container.innerHTML = recommendations.map(rec => `
        <li class="flex items-start">
            <i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
            <span class="text-gray-600">${rec}</span>
        </li>
    `).join('');
}

function updateLastUpdated() {
    const element = document.getElementById('lastUpdate');
    if (element) {
        element.textContent = 'Last updated: ' + new Date().toLocaleTimeString();
    }
}

// Error handling
function showError(message) {
    console.error(message);
    // You could implement a UI toast/notification system here
}

// Initialize real-time updates
function initializeRealTimeUpdates(interval = 5000) {
    async function update() {
        const metrics = await fetchMetrics();
        if (metrics) {
            updateActivityMetrics(metrics);
            updateRiskIndicator(metrics.risk_level);
            updateRecommendations(metrics.recommendations);
            updateLastUpdated();
        }
    }

    // Initial update
    update();

    // Set up periodic updates
    return setInterval(update, interval);
}

// Export functions for use in other scripts
window.BurnoutMonitor = {
    formatTime,
    formatNumber,
    formatDate,
    fetchMetrics,
    fetchHistory,
    initializeRealTimeUpdates,
    showError
};
