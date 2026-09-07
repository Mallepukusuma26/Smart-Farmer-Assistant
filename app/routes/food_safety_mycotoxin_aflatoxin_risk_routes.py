"""
FoodSafetyMycotoxinAflatoxinRiskEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.food_safety_mycotoxin_aflatoxin_risk_controller import FoodSafetyMycotoxinAflatoxinRiskEngineController

food_safety_mycotoxin_aflatoxin_risk_bp = Blueprint("food-safety-mycotoxin-aflatoxin-risk", __name__, url_prefix="/api/food-safety-mycotoxin-aflatoxin-risk")
controller = FoodSafetyMycotoxinAflatoxinRiskEngineController()

@food_safety_mycotoxin_aflatoxin_risk_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@food_safety_mycotoxin_aflatoxin_risk_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@food_safety_mycotoxin_aflatoxin_risk_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
