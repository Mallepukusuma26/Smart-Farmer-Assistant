"""
PrecisionAgThermalDroughtStressEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_thermal_drought_stress_mapper_controller import PrecisionAgThermalDroughtStressEngineController

precision_ag_thermal_drought_stress_mapper_bp = Blueprint("precision-ag-thermal-drought-stress-mapper", __name__, url_prefix="/api/precision-ag-thermal-drought-stress-mapper")
controller = PrecisionAgThermalDroughtStressEngineController()

@precision_ag_thermal_drought_stress_mapper_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_thermal_drought_stress_mapper_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_thermal_drought_stress_mapper_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
