"""
FAO-33 Water Production Function Yield Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_yield_water_production_function_controller import CropWaterYieldFunctionEngineController

crop_yield_water_production_function_engine_bp = Blueprint("crop-yield-water-production-function", __name__, url_prefix="/api/crop-yield-water-production-function")
controller = CropWaterYieldFunctionEngineController()

@crop_yield_water_production_function_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@crop_yield_water_production_function_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
