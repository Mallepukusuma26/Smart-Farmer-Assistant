/**
 * Smart Farmer Assistant — Pure JavaScript Canvas Charting Engine
 * Renders Bar, Line, Pie, and Gauge charts on HTML5 Canvas without external CDN dependencies.
 */

class SmartChart {
  static drawBarChart(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 400;
    const height = canvas.height = canvas.parentElement.clientHeight || 280;

    ctx.clearRect(0, 0, width, height);

    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    const maxValue = Math.max(...data, 10);

    const barWidth = (chartWidth / data.length) * 0.6;
    const barGap = (chartWidth / data.length) * 0.4;

    // Draw Axes
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    // Draw Bars
    data.forEach((val, i) => {
      const barHeight = (val / maxValue) * chartHeight;
      const x = padding + i * (barWidth + barGap) + barGap / 2;
      const y = height - padding - barHeight;

      // Gradient
      const gradient = ctx.createLinearGradient(0, y, 0, height - padding);
      gradient.addColorStop(0, options.color || '#2e7d32');
      gradient.addColorStop(1, '#a5d6a7');

      ctx.fillStyle = gradient;
      ctx.fillRect(x, y, barWidth, barHeight);

      // Labels
      ctx.fillStyle = '#64748b';
      ctx.font = '12px Outfit, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(labels[i] || '', x + barWidth / 2, height - padding + 20);

      // Values
      ctx.fillStyle = '#1e293b';
      ctx.fillText(val, x + barWidth / 2, y - 6);
    });
  }

  static drawLineChart(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 400;
    const height = canvas.height = canvas.parentElement.clientHeight || 280;

    ctx.clearRect(0, 0, width, height);

    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    const maxValue = Math.max(...data, 10);

    // Axes
    ctx.strokeStyle = '#e2e8f0';
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    // Plot Line
    ctx.strokeStyle = options.color || '#00897b';
    ctx.lineWidth = 3;
    ctx.beginPath();

    const points = data.map((val, i) => {
      const x = padding + (i / (data.length - 1 || 1)) * chartWidth;
      const y = height - padding - (val / maxValue) * chartHeight;
      return { x, y };
    });

    points.forEach((pt, i) => {
      if (i === 0) ctx.moveTo(pt.x, pt.y);
      else ctx.lineTo(pt.x, pt.y);
    });
    ctx.stroke();

    // Plot Dots
    points.forEach((pt, i) => {
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = options.color || '#00897b';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#64748b';
      ctx.font = '11px Outfit, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(labels[i] || '', pt.x, height - padding + 20);
    });
  }

  static drawGauge(canvasId, score, maxScore = 100) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 220;
    const height = canvas.height = canvas.parentElement.clientHeight || 160;

    const cx = width / 2;
    const cy = height - 20;
    const radius = Math.min(width, height) * 0.7;

    ctx.clearRect(0, 0, width, height);

    // Background Arc
    ctx.lineWidth = 14;
    ctx.strokeStyle = '#e2e8f0';
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, 0, false);
    ctx.stroke();

    // Score Arc
    const pct = Math.min(Math.max(score / maxScore, 0), 1);
    const endAngle = Math.PI + pct * Math.PI;

    let color = '#d32f2f'; // Red
    if (pct >= 0.7) color = '#2e7d32'; // Green
    else if (pct >= 0.4) color = '#f57c00'; // Amber

    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, endAngle, false);
    ctx.stroke();

    // Text score
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 24px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${score}/${maxScore}`, cx, cy - 10);
  }
}

window.SmartChart = SmartChart;
