// Smart Farmer Assistant — Chart.js Helper Script

function renderRadarSoilChart(elementId, n, p, k, ph, moisture) {
    const ctx = document.getElementById(elementId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Nitrogen', 'Phosphorus', 'Potassium', 'pH Score', 'Moisture %'],
            datasets: [{
                label: 'Current Soil Profile',
                data: [n, p, k, ph * 10, moisture * 2],
                fill: true,
                backgroundColor: 'rgba(45, 106, 79, 0.2)',
                borderColor: '#2d6a4f',
                pointBackgroundColor: '#1b4332'
            }]
        },
        options: {
            elements: { line: { borderWidth: 3 } }
        }
    });
}
