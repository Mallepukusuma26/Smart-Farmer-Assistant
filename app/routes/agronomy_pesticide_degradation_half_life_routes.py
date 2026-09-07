"""
AgronomyPesticideDegradationHalfLifeEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_pesticide_degradation_half_life_controller import AgronomyPesticideDegradationHalfLifeEngineController

agronomy_pesticide_degradation_half_life_bp = Blueprint("agronomy-pesticide-degradation-half-life", __name__, url_prefix="/api/agronomy-pesticide-degradation-half-life")
controller = AgronomyPesticideDegradationHalfLifeEngineController()

@agronomy_pesticide_degradation_half_life_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_pesticide_degradation_half_life_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
