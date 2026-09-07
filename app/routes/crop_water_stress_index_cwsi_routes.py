"""
CropWaterStressIndexCWSIEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_water_stress_index_cwsi_controller import CropWaterStressIndexCWSIEngineController

crop_water_stress_index_cwsi_bp = Blueprint("crop-water-stress-index-cwsi", __name__, url_prefix="/api/crop-water-stress-index-cwsi")
controller = CropWaterStressIndexCWSIEngineController()

@crop_water_stress_index_cwsi_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_water_stress_index_cwsi_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_water_stress_index_cwsi_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
