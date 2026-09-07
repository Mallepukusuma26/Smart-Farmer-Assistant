"""
CropRotationMultiSeasonSequenceEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_rotation_multi_season_sequence_controller import CropRotationMultiSeasonSequenceEngineController

crop_rotation_multi_season_sequence_bp = Blueprint("crop-rotation-multi-season-sequence", __name__, url_prefix="/api/crop-rotation-multi-season-sequence")
controller = CropRotationMultiSeasonSequenceEngineController()

@crop_rotation_multi_season_sequence_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_rotation_multi_season_sequence_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_rotation_multi_season_sequence_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
