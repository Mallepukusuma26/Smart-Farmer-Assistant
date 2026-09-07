/**
 * Smart Farmer Assistant — Farm & Field Spatial Manager JS Component
 * Handles field boundary coordinate mapping, acreage calculation, spatial field rendering,
 * and interactive plot selection on HTML5 Canvas.
 */

class FarmSpatialManager {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.fields = [];
    this.selectedField = null;
    this.initCanvas();
  }

  initCanvas() {
    this.width = this.canvas.width = this.canvas.parentElement.clientWidth || 600;
    this.height = this.canvas.height = this.canvas.parentElement.clientHeight || 400;
    this.bindEvents();
    this.render();
  }

  bindEvents() {
    this.canvas.addEventListener('click', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;
      this.handleCanvasClick(clickX, clickY);
    });
  }

  setFields(fieldsData) {
    this.fields = fieldsData.map((f, i) => ({
      id: f.id,
      name: f.name,
      area: f.area_acres || 5.0,
      crop: f.current_crop_name || 'Unassigned',
      color: this.getFieldColor(i),
      x: 40 + (i % 3) * 170,
      y: 40 + Math.floor(i / 3) * 120,
      width: 140,
      height: 90
    }));
    this.render();
  }

  getFieldColor(index) {
    const palette = ['#81c784', '#66bb6a', '#4caf50', '#388e3c', '#2e7d32', '#1b5e20'];
    return palette[index % palette.length];
  }

  handleCanvasClick(x, y) {
    const clicked = this.fields.find(f => 
      x >= f.x && x <= f.x + f.width && y >= f.y && y <= f.y + f.height
    );
    if (clicked) {
      this.selectedField = clicked;
      this.render();
      if (typeof this.onFieldSelected === 'function') {
        this.onFieldSelected(clicked);
      }
    }
  }

  render() {
    if (!this.ctx) return;
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Draw Farm Grid Outline
    this.ctx.strokeStyle = '#e2e8f0';
    this.ctx.lineWidth = 1;
    for (let x = 0; x < this.width; x += 30) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.height);
      this.ctx.stroke();
    }
    for (let y = 0; y < this.height; y += 30) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.width, y);
      this.ctx.stroke();
    }

    // Render Field Plots
    this.fields.forEach(f => {
      const isSelected = this.selectedField && this.selectedField.id === f.id;

      // Plot Box
      this.ctx.fillStyle = f.color;
      this.ctx.globalAlpha = isSelected ? 0.9 : 0.65;
      this.ctx.fillRect(f.x, f.y, f.width, f.height);
      this.ctx.globalAlpha = 1.0;

      // Border
      this.ctx.strokeStyle = isSelected ? '#1b5e20' : '#ffffff';
      this.ctx.lineWidth = isSelected ? 3 : 2;
      this.ctx.strokeRect(f.x, f.y, f.width, f.height);

      // Label Text
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = 'bold 13px Outfit, sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText(f.name, f.x + f.width / 2, f.y + 35);

      this.ctx.font = '11px Outfit, sans-serif';
      this.ctx.fillText(`${f.area} Acres`, f.x + f.width / 2, f.y + 55);
      this.ctx.fillText(f.crop, f.x + f.width / 2, f.y + 72);
    });

    if (this.fields.length === 0) {
      this.ctx.fillStyle = '#94a3b8';
      this.ctx.font = '14px Outfit, sans-serif';
      this.ctx.textAlign = 'center';
      this.ctx.fillText('No field plots registered for this farm.', this.width / 2, this.height / 2);
    }
  }
}

window.FarmSpatialManager = FarmSpatialManager;
