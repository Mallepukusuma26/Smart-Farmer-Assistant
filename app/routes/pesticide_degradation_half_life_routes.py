"""
Pesticide Environmental Fate & Half-Life Degradation Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.pesticide_degradation_half_life_controller import PesticideFateEngineController

pesticide_degradation_half_life_engine_bp = Blueprint("pesticide-degradation-half-life", __name__, url_prefix="/api/pesticide-degradation-half-life")
controller = PesticideFateEngineController()

@pesticide_degradation_half_life_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@pesticide_degradation_half_life_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
