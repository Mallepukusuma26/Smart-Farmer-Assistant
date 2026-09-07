"""
Multi-Year Crop Rotation Soil Depletion Penalty Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_rotation_soil_depletion_controller import CropRotationDepletionEngineController

crop_rotation_soil_depletion_engine_bp = Blueprint("crop-rotation-soil-depletion", __name__, url_prefix="/api/crop-rotation-soil-depletion")
controller = CropRotationDepletionEngineController()

@crop_rotation_soil_depletion_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@crop_rotation_soil_depletion_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
