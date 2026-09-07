"""
FoodSafetyColdChainQ10SpoilageEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.food_safety_cold_chain_q10_spoilage_controller import FoodSafetyColdChainQ10SpoilageEngineController

food_safety_cold_chain_q10_spoilage_bp = Blueprint("food-safety-cold-chain-q10-spoilage", __name__, url_prefix="/api/food-safety-cold-chain-q10-spoilage")
controller = FoodSafetyColdChainQ10SpoilageEngineController()

@food_safety_cold_chain_q10_spoilage_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@food_safety_cold_chain_q10_spoilage_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@food_safety_cold_chain_q10_spoilage_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
