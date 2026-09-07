"""
FoodSafetyPesticideMRLComplianceEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.food_safety_pesticide_mrl_compliance_controller import FoodSafetyPesticideMRLComplianceEngineController

food_safety_pesticide_mrl_compliance_bp = Blueprint("food-safety-pesticide-mrl-compliance", __name__, url_prefix="/api/food-safety-pesticide-mrl-compliance")
controller = FoodSafetyPesticideMRLComplianceEngineController()

@food_safety_pesticide_mrl_compliance_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@food_safety_pesticide_mrl_compliance_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@food_safety_pesticide_mrl_compliance_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
