"""
AgronomyFarmFinancialMonteCarloEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_farm_financial_monte_carlo_controller import AgronomyFarmFinancialMonteCarloEngineController

agronomy_farm_financial_monte_carlo_bp = Blueprint("agronomy-farm-financial-monte-carlo", __name__, url_prefix="/api/agronomy-farm-financial-monte-carlo")
controller = AgronomyFarmFinancialMonteCarloEngineController()

@agronomy_farm_financial_monte_carlo_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_farm_financial_monte_carlo_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
