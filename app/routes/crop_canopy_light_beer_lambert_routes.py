"""
CropCanopyLightBeerLambertEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_canopy_light_beer_lambert_controller import CropCanopyLightBeerLambertEngineController

crop_canopy_light_beer_lambert_bp = Blueprint("crop-canopy-light-beer-lambert", __name__, url_prefix="/api/crop-canopy-light-beer-lambert")
controller = CropCanopyLightBeerLambertEngineController()

@crop_canopy_light_beer_lambert_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_canopy_light_beer_lambert_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_canopy_light_beer_lambert_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
