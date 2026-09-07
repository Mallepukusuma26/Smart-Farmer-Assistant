"""
Phosphorus Sorption Isotherm & Availability Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_phosphorus_sorption_controller import PhosphorusSorptionEngineController

soil_phosphorus_sorption_engine_bp = Blueprint("soil-phosphorus-sorption", __name__, url_prefix="/api/soil-phosphorus-sorption")
controller = PhosphorusSorptionEngineController()

@soil_phosphorus_sorption_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@soil_phosphorus_sorption_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
