"""
Build Huge Fullstack Files for Smart Farmer Assistant.
Creates production files across controllers, routes, schemas, JS modules, and Jinja2 templates.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create(path: str, content: str):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created {path} ({len(content.splitlines())} lines)")

# ----------------------------------------------------
# 1. CONTROLLERS & ROUTES (app/controllers/ & app/routes/)
# ----------------------------------------------------

create("app/controllers/crop_water_stress_controller.py", '''"""
Crop Water Stress Index Controller.
API endpoints for thermal canopy temperature water stress evaluation.
"""

from flask import jsonify, request
from app.services.agronomy.crop_water_stress_index_engine import CropWaterStressIndexEngine

class CropWaterStressController:
    """Controller for CWSI evaluation endpoints."""

    def __init__(self, engine=None):
        self.engine = engine or CropWaterStressIndexEngine()

    def evaluate_stress(self):
        """API endpoint to calculate CWSI from thermal sensor readings."""
        data = request.get_json() or {}
        tc = float(data.get("canopy_temp", 28.5))
        ta = float(data.get("air_temp", 26.0))
        rh = float(data.get("rh_pct", 55.0))

        res = self.engine.calculate_cwsi(tc, ta, rh)
        return jsonify({"success": True, "cwsi_evaluation": res})
''')

create("app/routes/crop_water_stress_routes.py", '''"""
Crop Water Stress Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_water_stress_controller import CropWaterStressController

crop_water_stress_bp = Blueprint("crop_water_stress", __name__, url_prefix="/api/crop-water-stress")
controller = CropWaterStressController()

@crop_water_stress_bp.route("/evaluate", methods=["POST"])
def evaluate():
    return controller.evaluate_stress()
''')

create("app/controllers/pest_economic_threshold_controller.py", '''"""
Pest Economic Threshold Controller.
API endpoints for insect pest Economic Injury Level (EIL) calculations.
"""

from flask import jsonify, request
from app.services.agronomy.pest_population_degree_day_engine import PestPopulationDegreeDayEngine

class PestEconomicThresholdController:
    """Controller for pest economic threshold endpoints."""

    def __init__(self, engine=None):
        self.engine = engine or PestPopulationDegreeDayEngine()

    def calculate_eil(self):
        """Calculate EIL and economic threshold for pest control action."""
        data = request.get_json() or {}
        cost = float(data.get("control_cost_ha", 45.0))
        price = float(data.get("market_price_ton", 220.0))
        loss = float(data.get("yield_loss_per_pest", 0.05))

        res = self.engine.calculate_economic_injury_level(cost, price, loss)
        return jsonify({"success": True, "eil_calculation": res})
''')

create("app/routes/pest_economic_threshold_routes.py", '''"""
Pest Economic Threshold Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.pest_economic_threshold_controller import PestEconomicThresholdController

pest_bp = Blueprint("pest_economic_threshold", __name__, url_prefix="/api/pest-threshold")
controller = PestEconomicThresholdController()

@pest_bp.route("/calculate-eil", methods=["POST"])
def calculate_eil():
    return controller.calculate_eil()
''')

# ----------------------------------------------------
# 2. JAVASCRIPT LOGIC MODULES (frontend/static/js/)
# ----------------------------------------------------

create("frontend/static/js/crop_water_stress_visualizer.js", '''/**
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
''')

create("frontend/static/js/pest_scouting_tracker.js", '''/**
 * Insect Pest Scouting & Economic Threshold Client Tracker.
 */

const PestScoutingTracker = {
    evaluatePestDensity: function(scoutedCount, squareMeters, ethresh) {
        const density = (scoutedCount / squareMeters).toFixed(2);
        const actionNeeded = parseFloat(density) >= parseFloat(ethresh);

        return {
            pestDensityM2: density,
            actionRequired: actionNeeded,
            statusBadgeClass: actionNeeded ? 'badge bg-danger' : 'badge bg-success',
            statusMessage: actionNeeded ? 'ALERT: Scouted density exceeds Economic Threshold!' : 'Pest population is within safe threshold.'
        };
    }
};
''')

# ----------------------------------------------------
# 3. HTML TEMPLATES (frontend/templates/farmer/)
# ----------------------------------------------------

create("frontend/templates/farmer/water_stress.html", '''{% extends "base.html" %}
{% block title %}Crop Water Stress (CWSI) — Smart Farmer Assistant{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="h3 mb-3 text-gray-800">Thermal Crop Water Stress Index (CWSI)</div>
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-3 p-4 text-center">
                <h5 class="fw-bold">Field A1 Canopy Thermal Gauge</h5>
                <canvas id="cwsiGaugeCanvas" width="300" height="180" class="mx-auto my-3"></canvas>
                <div class="alert alert-info mb-0">Current CWSI: <strong>0.32 (Mild Stress)</strong></div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-3 p-4">
                <h5 class="fw-bold">Sensor Inputs</h5>
                <form id="cwsiForm">
                    <div class="mb-3">
                        <label class="form-label">Canopy Temp (°C)</label>
                        <input type="number" step="0.1" class="form-control" value="28.5" id="inputTc"/>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Air Temp (°C)</label>
                        <input type="number" step="0.1" class="form-control" value="26.0" id="inputTa"/>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Relative Humidity (%)</label>
                        <input type="number" class="form-control" value="55" id="inputRh"/>
                    </div>
                    <button type="button" class="btn btn-primary w-100" onclick="calculateCWSI()">Evaluate CWSI</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
''')

create("frontend/templates/farmer/pest_scouting.html", '''{% extends "base.html" %}
{% block title %}Pest Scouting & Economic Threshold — Smart Farmer Assistant{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="h3 mb-3 text-gray-800">Insect Pest Scouting & Economic Injury Level (EIL)</div>
    <div class="card border-0 shadow-sm rounded-3 p-4">
        <h5 class="fw-bold mb-3">Scouting Logs & Action Thresholds</h5>
        <div class="table-responsive">
            <table class="table align-middle custom-table">
                <thead class="table-light">
                    <tr>
                        <th>Pest Name</th>
                        <th>Crop Field</th>
                        <th>Scouted Density</th>
                        <th>Economic Threshold</th>
                        <th>Status</th>
                        <th>Recommended Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Fall Armyworm</td>
                        <td>Maize Field B1</td>
                        <td>4.2 / m²</td>
                        <td>3.0 / m²</td>
                        <td><span class="badge bg-danger">Action Required</span></td>
                        <td>Apply Neem-based Azadirachtin spray immediately.</td>
                    </tr>
                    <tr>
                        <td>Aphids</td>
                        <td>Wheat Field A2</td>
                        <td>1.1 / m²</td>
                        <td>5.0 / m²</td>
                        <td><span class="badge bg-success">Safe</span></td>
                        <td>Monitor again in 5 days.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
''')

print("Created huge fullstack files batch.")
