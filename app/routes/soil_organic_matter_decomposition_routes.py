"""
Soil Organic Matter Decomposition Kinetics Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_organic_matter_decomposition_controller import SOMDecompositionEngineController

soil_organic_matter_decomposition_engine_bp = Blueprint("soil-organic-matter-decomposition", __name__, url_prefix="/api/soil-organic-matter-decomposition")
controller = SOMDecompositionEngineController()

@soil_organic_matter_decomposition_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@soil_organic_matter_decomposition_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
