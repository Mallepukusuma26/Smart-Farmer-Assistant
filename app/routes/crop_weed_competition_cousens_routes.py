"""
CropWeedCompetitionCousensEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_weed_competition_cousens_controller import CropWeedCompetitionCousensEngineController

crop_weed_competition_cousens_bp = Blueprint("crop-weed-competition-cousens", __name__, url_prefix="/api/crop-weed-competition-cousens")
controller = CropWeedCompetitionCousensEngineController()

@crop_weed_competition_cousens_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_weed_competition_cousens_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_weed_competition_cousens_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
