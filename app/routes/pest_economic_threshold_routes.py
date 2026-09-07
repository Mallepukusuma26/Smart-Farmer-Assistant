"""
Pest Economic Threshold Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.pest_economic_threshold_controller import PestEconomicThresholdController

pest_bp = Blueprint("pest_economic_threshold", __name__, url_prefix="/api/pest-threshold")
controller = PestEconomicThresholdController()

@pest_bp.route("/calculate-eil", methods=["POST"])
def calculate_eil():
    return controller.calculate_eil()
