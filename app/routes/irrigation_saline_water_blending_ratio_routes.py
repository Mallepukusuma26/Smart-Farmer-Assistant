"""
IrrigationSalineWaterBlendingRatioEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.irrigation_saline_water_blending_ratio_controller import IrrigationSalineWaterBlendingRatioEngineController

irrigation_saline_water_blending_ratio_bp = Blueprint("irrigation-saline-water-blending-ratio", __name__, url_prefix="/api/irrigation-saline-water-blending-ratio")
controller = IrrigationSalineWaterBlendingRatioEngineController()

@irrigation_saline_water_blending_ratio_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@irrigation_saline_water_blending_ratio_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@irrigation_saline_water_blending_ratio_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
