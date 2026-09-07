"""
FarmEnterpriseBudgetingCalculatorEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.farm_enterprise_budgeting_calculator_controller import FarmEnterpriseBudgetingCalculatorEngineController

farm_enterprise_budgeting_calculator_bp = Blueprint("farm-enterprise-budgeting-calculator", __name__, url_prefix="/api/farm-enterprise-budgeting-calculator")
controller = FarmEnterpriseBudgetingCalculatorEngineController()

@farm_enterprise_budgeting_calculator_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@farm_enterprise_budgeting_calculator_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@farm_enterprise_budgeting_calculator_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
