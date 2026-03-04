// Chart.js CDN loader and fallback
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    script.onload = function() {
        if (typeof Chart === 'undefined') {
            alert('Chart.js failed to load.');
        }
    };
    document.head.appendChild(script);
})();
function updateDashboardAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            const alertContainer = document.getElementById('system-alerts'); // Ensure this ID is in dashboard.html
            
            if (data.level !== 'NORMAL' && data.type !== 'None') {
                // UI par alert dikhayein
                alertContainer.innerHTML = `
                    <div class="alert-box ${data.level.toLowerCase()}">
                        <h3>🚨 ${data.type} DETECTED</h3>
                        <p>${data.message}</p>
                    </div>
                `;
                console.log("Anomaly Detected:", data.type);
            } else {
                alertContainer.innerHTML = '<p class="safe-msg">✅ All Systems Operational</p>';
            }
        })
        .catch(error => console.error('Error fetching alerts:', error));
}

// Har 2 second mein alerts update karein
setInterval(updateDashboardAlerts, 2000);
