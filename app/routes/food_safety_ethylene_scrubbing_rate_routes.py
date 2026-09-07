"""
FoodSafetyEthyleneScrubbingRateEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.food_safety_ethylene_scrubbing_rate_controller import FoodSafetyEthyleneScrubbingRateEngineController

food_safety_ethylene_scrubbing_rate_bp = Blueprint("food-safety-ethylene-scrubbing-rate", __name__, url_prefix="/api/food-safety-ethylene-scrubbing-rate")
controller = FoodSafetyEthyleneScrubbingRateEngineController()

@food_safety_ethylene_scrubbing_rate_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@food_safety_ethylene_scrubbing_rate_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@food_safety_ethylene_scrubbing_rate_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
