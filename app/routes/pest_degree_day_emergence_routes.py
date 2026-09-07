"""
Pest Degree-Day Emergence & Economic Injury Level Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.pest_degree_day_emergence_controller import PestEmergenceEILEngineController

pest_degree_day_emergence_engine_bp = Blueprint("pest-degree-day-emergence", __name__, url_prefix="/api/pest-degree-day-emergence")
controller = PestEmergenceEILEngineController()

@pest_degree_day_emergence_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@pest_degree_day_emergence_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
