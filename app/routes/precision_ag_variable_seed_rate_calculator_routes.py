"""
PrecisionAgVariableSeedRateEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_variable_seed_rate_calculator_controller import PrecisionAgVariableSeedRateEngineController

precision_ag_variable_seed_rate_calculator_bp = Blueprint("precision-ag-variable-seed-rate-calculator", __name__, url_prefix="/api/precision-ag-variable-seed-rate-calculator")
controller = PrecisionAgVariableSeedRateEngineController()

@precision_ag_variable_seed_rate_calculator_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_variable_seed_rate_calculator_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_variable_seed_rate_calculator_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
