/**
 * Smart Farmer Assistant — Farm Financial Calculator Component
 * Calculates total expenses, gross revenue, net profit margin, ROI %, and cost-per-acre in real time.
 */

class FinanceTracker {
  static calculateFinancials(seed, fert, pest, labour, irrig, mach, other, area, yieldVal, price) {
    const totalExp = (seed + fert + pest + labour + irrig + mach + other) * area;
    const grossRev = (yieldVal * area) * price;
    const netProfit = grossRev - totalExp;
    const roi = totalExp > 0 ? (netProfit / totalExp) * 100 : 0;
    const costPerAcre = area > 0 ? totalExp / area : 0;
    const profitPerAcre = area > 0 ? netProfit / area : 0;

    return {
      totalExpenses: Math.round(totalExp * 100) / 100,
      grossRevenue: Math.round(grossRev * 100) / 100,
      netProfit: Math.round(netProfit * 100) / 100,
      roiPercentage: Math.round(roi * 100) / 100,
      costPerAcre: Math.round(costPerAcre * 100) / 100,
      profitPerAcre: Math.round(profitPerAcre * 100) / 100,
      isProfitable: netProfit > 0
    };
  }

  static bindLiveCalculator(formId, resultContainerId) {
    const form = document.getElementById(formId);
    const container = document.getElementById(resultContainerId);
    if (!form || !container) return;

    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
      input.addEventListener('input', () => {
        const seed = parseFloat(form.querySelector('[name="seed_cost"]')?.value || 0);
        const fert = parseFloat(form.querySelector('[name="fertilizer_cost"]')?.value || 0);
        const pest = parseFloat(form.querySelector('[name="pesticide_cost"]')?.value || 0);
        const labour = parseFloat(form.querySelector('[name="labour_cost"]')?.value || 0);
        const irrig = parseFloat(form.querySelector('[name="irrigation_cost"]')?.value || 0);
        const mach = parseFloat(form.querySelector('[name="machinery_cost"]')?.value || 0);
        const other = parseFloat(form.querySelector('[name="other_cost"]')?.value || 0);
        const area = parseFloat(form.querySelector('[name="land_area_acres"]')?.value || 1);
        const yieldVal = parseFloat(form.querySelector('[name="expected_yield_per_acre"]')?.value || 0);
        const price = parseFloat(form.querySelector('[name="expected_market_price_per_tonne"]')?.value || 0);

        const res = FinanceTracker.calculateFinancials(seed, fert, pest, labour, irrig, mach, other, area, yieldVal, price);

        container.innerHTML = `
          <div class="row g-3 text-center">
            <div class="col-4">
              <div class="p-3 bg-light rounded-3 border">
                <span class="d-block text-muted fs-8">TOTAL EXPENSES</span>
                <span class="fs-5 fw-bold text-danger">$${res.totalExpenses.toLocaleString()}</span>
              </div>
            </div>
            <div class="col-4">
              <div class="p-3 bg-light rounded-3 border">
                <span class="d-block text-muted fs-8">GROSS REVENUE</span>
                <span class="fs-5 fw-bold text-success">$${res.grossRevenue.toLocaleString()}</span>
              </div>
            </div>
            <div class="col-4">
              <div class="p-3 bg-light rounded-3 border">
                <span class="d-block text-muted fs-8">NET PROFIT</span>
                <span class="fs-5 fw-bold ${res.isProfitable ? 'text-success' : 'text-danger'}">$${res.netProfit.toLocaleString()} (${res.roiPercentage}%)</span>
              </div>
            </div>
          </div>
        `;
      });
    });
  }
}

window.FinanceTracker = FinanceTracker;
