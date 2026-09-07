"""
CropVernalizationChillingHoursEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_vernalization_chilling_hours_controller import CropVernalizationChillingHoursEngineController

crop_vernalization_chilling_hours_bp = Blueprint("crop-vernalization-chilling-hours", __name__, url_prefix="/api/crop-vernalization-chilling-hours")
controller = CropVernalizationChillingHoursEngineController()

@crop_vernalization_chilling_hours_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_vernalization_chilling_hours_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_vernalization_chilling_hours_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
