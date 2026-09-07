"""
RUSLE2 Soil Erosion Loss & Erosivity Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_erosion_rusle2_controller import RUSLE2SoilErosionEngineController

soil_erosion_rusle2_engine_bp = Blueprint("soil-erosion-rusle2", __name__, url_prefix="/api/soil-erosion-rusle2")
controller = RUSLE2SoilErosionEngineController()

@soil_erosion_rusle2_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@soil_erosion_rusle2_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
