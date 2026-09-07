"""
CropLodgingRiskStemStrengthEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_lodging_risk_stem_strength_controller import CropLodgingRiskStemStrengthEngineController

crop_lodging_risk_stem_strength_bp = Blueprint("crop-lodging-risk-stem-strength", __name__, url_prefix="/api/crop-lodging-risk-stem-strength")
controller = CropLodgingRiskStemStrengthEngineController()

@crop_lodging_risk_stem_strength_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_lodging_risk_stem_strength_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_lodging_risk_stem_strength_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
