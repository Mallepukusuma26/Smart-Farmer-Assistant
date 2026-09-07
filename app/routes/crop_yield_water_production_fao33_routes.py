"""
CropYieldWaterProductionFAO33Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_yield_water_production_fao33_controller import CropYieldWaterProductionFAO33EngineController

crop_yield_water_production_fao33_bp = Blueprint("crop-yield-water-production-fao33", __name__, url_prefix="/api/crop-yield-water-production-fao33")
controller = CropYieldWaterProductionFAO33EngineController()

@crop_yield_water_production_fao33_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_yield_water_production_fao33_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_yield_water_production_fao33_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
