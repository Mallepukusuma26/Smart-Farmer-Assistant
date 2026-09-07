"""
SoilErosionRUSLEErosivityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_erosion_rusle_erosivity_controller import SoilErosionRUSLEErosivityEngineController

soil_erosion_rusle_erosivity_bp = Blueprint("soil-erosion-rusle-erosivity", __name__, url_prefix="/api/soil-erosion-rusle-erosivity")
controller = SoilErosionRUSLEErosivityEngineController()

@soil_erosion_rusle_erosivity_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_erosion_rusle_erosivity_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_erosion_rusle_erosivity_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
