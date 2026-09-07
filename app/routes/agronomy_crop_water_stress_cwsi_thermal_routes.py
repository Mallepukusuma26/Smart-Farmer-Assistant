"""
AgronomyCropWaterStressCWSIThermalEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_crop_water_stress_cwsi_thermal_controller import AgronomyCropWaterStressCWSIThermalEngineController

agronomy_crop_water_stress_cwsi_thermal_bp = Blueprint("agronomy-crop-water-stress-cwsi-thermal", __name__, url_prefix="/api/agronomy-crop-water-stress-cwsi-thermal")
controller = AgronomyCropWaterStressCWSIThermalEngineController()

@agronomy_crop_water_stress_cwsi_thermal_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_crop_water_stress_cwsi_thermal_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
