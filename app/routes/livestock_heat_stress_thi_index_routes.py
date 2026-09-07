"""
LivestockHeatStressTHIEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.livestock_heat_stress_thi_index_controller import LivestockHeatStressTHIEngineController

livestock_heat_stress_thi_index_bp = Blueprint("livestock-heat-stress-thi-index", __name__, url_prefix="/api/livestock-heat-stress-thi-index")
controller = LivestockHeatStressTHIEngineController()

@livestock_heat_stress_thi_index_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@livestock_heat_stress_thi_index_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@livestock_heat_stress_thi_index_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
