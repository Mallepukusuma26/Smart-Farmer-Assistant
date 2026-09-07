"""
SeedHarvestMoistureShatterRiskEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.seed_harvest_moisture_shatter_risk_controller import SeedHarvestMoistureShatterRiskEngineController

seed_harvest_moisture_shatter_risk_bp = Blueprint("seed-harvest-moisture-shatter-risk", __name__, url_prefix="/api/seed-harvest-moisture-shatter-risk")
controller = SeedHarvestMoistureShatterRiskEngineController()

@seed_harvest_moisture_shatter_risk_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@seed_harvest_moisture_shatter_risk_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@seed_harvest_moisture_shatter_risk_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
