"""
AgronomyCropWaterStressIndexThermalEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_crop_water_stress_index_thermal_controller import AgronomyCropWaterStressIndexThermalEngineController

agronomy_crop_water_stress_index_thermal_bp = Blueprint("agronomy-crop-water-stress-index-thermal", __name__, url_prefix="/api/agronomy-crop-water-stress-index-thermal")
ctrl = AgronomyCropWaterStressIndexThermalEngineController()

@agronomy_crop_water_stress_index_thermal_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
