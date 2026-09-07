"""
Nitrogen Volatilization & Denitrification Losses Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertilizer_volatilization_denitrification_controller import NitrogenLossesEngineController

fertilizer_volatilization_denitrification_engine_bp = Blueprint("fertilizer-volatilization-denitrification", __name__, url_prefix="/api/fertilizer-volatilization-denitrification")
controller = NitrogenLossesEngineController()

@fertilizer_volatilization_denitrification_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@fertilizer_volatilization_denitrification_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
