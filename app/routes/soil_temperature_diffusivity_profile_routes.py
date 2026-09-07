"""
SoilTemperatureDiffusivityProfileEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_temperature_diffusivity_profile_controller import SoilTemperatureDiffusivityProfileEngineController

soil_temperature_diffusivity_profile_bp = Blueprint("soil-temperature-diffusivity-profile", __name__, url_prefix="/api/soil-temperature-diffusivity-profile")
controller = SoilTemperatureDiffusivityProfileEngineController()

@soil_temperature_diffusivity_profile_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_temperature_diffusivity_profile_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_temperature_diffusivity_profile_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
