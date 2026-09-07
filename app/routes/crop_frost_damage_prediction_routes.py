"""
CropFrostDamagePredictionEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_frost_damage_prediction_controller import CropFrostDamagePredictionEngineController

crop_frost_damage_prediction_bp = Blueprint("crop-frost-damage-prediction", __name__, url_prefix="/api/crop-frost-damage-prediction")
controller = CropFrostDamagePredictionEngineController()

@crop_frost_damage_prediction_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_frost_damage_prediction_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_frost_damage_prediction_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
