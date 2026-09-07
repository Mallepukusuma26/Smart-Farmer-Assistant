"""
SafetyFarmNoiseDecibelExposureEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.safety_farm_noise_decibel_exposure_controller import SafetyFarmNoiseDecibelExposureEngineController

safety_farm_noise_decibel_exposure_bp = Blueprint("safety-farm-noise-decibel-exposure", __name__, url_prefix="/api/safety-farm-noise-decibel-exposure")
controller = SafetyFarmNoiseDecibelExposureEngineController()

@safety_farm_noise_decibel_exposure_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@safety_farm_noise_decibel_exposure_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@safety_farm_noise_decibel_exposure_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
