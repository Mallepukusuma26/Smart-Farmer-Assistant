"""
CropSeedSowingRateCalculatorEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_seed_sowing_rate_calculator_controller import CropSeedSowingRateCalculatorEngineController

crop_seed_sowing_rate_calculator_bp = Blueprint("crop-seed-sowing-rate-calculator", __name__, url_prefix="/api/crop-seed-sowing-rate-calculator")
controller = CropSeedSowingRateCalculatorEngineController()

@crop_seed_sowing_rate_calculator_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_seed_sowing_rate_calculator_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_seed_sowing_rate_calculator_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
