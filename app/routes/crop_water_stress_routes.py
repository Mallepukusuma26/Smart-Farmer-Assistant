"""
Crop Water Stress Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_water_stress_controller import CropWaterStressController

crop_water_stress_bp = Blueprint("crop_water_stress", __name__, url_prefix="/api/crop-water-stress")
controller = CropWaterStressController()

@crop_water_stress_bp.route("/evaluate", methods=["POST"])
def evaluate():
    return controller.evaluate_stress()
