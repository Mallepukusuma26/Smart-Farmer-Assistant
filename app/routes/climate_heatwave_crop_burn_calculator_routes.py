"""
ClimateHeatwaveCropBurnEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.climate_heatwave_crop_burn_calculator_controller import ClimateHeatwaveCropBurnEngineController

climate_heatwave_crop_burn_calculator_bp = Blueprint("climate-heatwave-crop-burn-calculator", __name__, url_prefix="/api/climate-heatwave-crop-burn-calculator")
controller = ClimateHeatwaveCropBurnEngineController()

@climate_heatwave_crop_burn_calculator_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@climate_heatwave_crop_burn_calculator_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@climate_heatwave_crop_burn_calculator_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
