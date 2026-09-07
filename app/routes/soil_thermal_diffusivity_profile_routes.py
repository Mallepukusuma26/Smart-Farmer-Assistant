"""
Soil Temperature Depth Profile & Thermal Diffusivity Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_thermal_diffusivity_profile_controller import SoilThermalProfileEngineController

soil_thermal_diffusivity_profile_engine_bp = Blueprint("soil-thermal-diffusivity-profile", __name__, url_prefix="/api/soil-thermal-diffusivity-profile")
controller = SoilThermalProfileEngineController()

@soil_thermal_diffusivity_profile_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@soil_thermal_diffusivity_profile_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
