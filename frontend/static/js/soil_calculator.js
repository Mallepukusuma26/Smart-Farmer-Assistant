/**
 * Smart Farmer Assistant — Soil Health & NPK Calculator Component
 * Interactive visual indicators for Nitrogen, Phosphorus, Potassium, pH,
 * Organic Carbon, and Electrical Conductivity parameters.
 */

class SoilHealthCalculator {
  static renderNPKIndicators(containerId, n, p, k) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
      <div class="npk-grid d-flex gap-3 justify-content-between">
        <div class="npk-card text-center p-3 rounded-3 border bg-white flex-fill">
          <span class="d-block text-muted fs-8 fw-bold">NITROGEN (N)</span>
          <span class="fs-4 fw-bold text-success">${n} <small class="fs-8 text-muted">kg/ha</small></span>
          <div class="progress mt-2" style="height: 6px;">
            <div class="progress-bar bg-success" style="width: ${Math.min((n / 200) * 100, 100)}%;"></div>
          </div>
          <span class="fs-8 text-muted mt-1 d-block">${SoilHealthCalculator.getRating('N', n)}</span>
        </div>
        <div class="npk-card text-center p-3 rounded-3 border bg-white flex-fill">
          <span class="d-block text-muted fs-8 fw-bold">PHOSPHORUS (P)</span>
          <span class="fs-4 fw-bold text-warning">${p} <small class="fs-8 text-muted">kg/ha</small></span>
          <div class="progress mt-2" style="height: 6px;">
            <div class="progress-bar bg-warning" style="width: ${Math.min((p / 100) * 100, 100)}%;"></div>
          </div>
          <span class="fs-8 text-muted mt-1 d-block">${SoilHealthCalculator.getRating('P', p)}</span>
        </div>
        <div class="npk-card text-center p-3 rounded-3 border bg-white flex-fill">
          <span class="d-block text-muted fs-8 fw-bold">POTASSIUM (K)</span>
          <span class="fs-4 fw-bold text-info">${k} <small class="fs-8 text-muted">kg/ha</small></span>
          <div class="progress mt-2" style="height: 6px;">
            <div class="progress-bar bg-info" style="width: ${Math.min((k / 300) * 100, 100)}%;"></div>
          </div>
          <span class="fs-8 text-muted mt-1 d-block">${SoilHealthCalculator.getRating('K', k)}</span>
        </div>
      </div>
    `;
  }

  static getRating(param, value) {
    if (param === 'N') {
      if (value < 50) return 'Low Deficiency';
      if (value <= 150) return 'Optimal Range';
      return 'High Richness';
    }
    if (param === 'P') {
      if (value < 20) return 'Low Deficiency';
      if (value <= 60) return 'Optimal Range';
      return 'High Richness';
    }
    if (param === 'K') {
      if (value < 40) return 'Low Deficiency';
      if (value <= 180) return 'Optimal Range';
      return 'High Richness';
    }
    return 'Normal';
  }

  static calculateHealthScore(n, p, k, ph, organicCarbon) {
    let score = 50;
    if (n >= 50 && n <= 150) score += 10;
    if (p >= 20 && p <= 60) score += 10;
    if (k >= 40 && k <= 180) score += 10;
    if (ph >= 6.0 && ph <= 7.5) score += 10;
    if (organicCarbon >= 0.5) score += 10;
    return Math.min(score, 100);
  }
}

window.SoilHealthCalculator = SoilHealthCalculator;
