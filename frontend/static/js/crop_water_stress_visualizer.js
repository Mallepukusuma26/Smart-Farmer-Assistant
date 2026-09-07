/**
 * Crop Water Stress Index (CWSI) Thermal Gauge & Charting Engine.
 */

class CWSIChartVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
    }

    renderGauge(cwsiValue) {
        if (!this.canvas) return;
        const ctx = this.canvas.getContext('2d');
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw background arc
        ctx.beginPath();
        ctx.arc(150, 150, 100, Math.PI, 2 * Math.PI);
        ctx.lineWidth = 20;
        ctx.strokeStyle = '#e2e8f0';
        ctx.stroke();

        // Draw value arc
        const color = cwsiValue < 0.3 ? '#16a34a' : (cwsiValue < 0.6 ? '#eab308' : '#dc2626');
        ctx.beginPath();
        ctx.arc(150, 150, 100, Math.PI, Math.PI + (cwsiValue * Math.PI));
        ctx.lineWidth = 20;
        ctx.strokeStyle = color;
        ctx.stroke();

        // Text value
        ctx.font = 'bold 24px sans-serif';
        ctx.fillStyle = '#0f172a';
        ctx.textAlign = 'center';
        ctx.fillText(`CWSI: ${cwsiValue}`, 150, 130);
    }
}
