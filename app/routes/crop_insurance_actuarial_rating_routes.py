"""
CropInsuranceActuarialRatingEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_insurance_actuarial_rating_controller import CropInsuranceActuarialRatingEngineController

crop_insurance_actuarial_rating_bp = Blueprint("crop-insurance-actuarial-rating", __name__, url_prefix="/api/crop-insurance-actuarial-rating")
controller = CropInsuranceActuarialRatingEngineController()

@crop_insurance_actuarial_rating_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_insurance_actuarial_rating_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_insurance_actuarial_rating_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
