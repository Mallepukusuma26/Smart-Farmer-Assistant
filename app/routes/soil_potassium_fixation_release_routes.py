"""
SoilPotassiumFixationReleaseEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_potassium_fixation_release_controller import SoilPotassiumFixationReleaseEngineController

soil_potassium_fixation_release_bp = Blueprint("soil-potassium-fixation-release", __name__, url_prefix="/api/soil-potassium-fixation-release")
controller = SoilPotassiumFixationReleaseEngineController()

@soil_potassium_fixation_release_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_potassium_fixation_release_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_potassium_fixation_release_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
