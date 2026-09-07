"""
IPMFungicideResistanceAntiStrategyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.ipm_fungicide_resistance_anti_strategy_controller import IPMFungicideResistanceAntiStrategyEngineController

ipm_fungicide_resistance_anti_strategy_bp = Blueprint("ipm-fungicide-resistance-anti-strategy", __name__, url_prefix="/api/ipm-fungicide-resistance-anti-strategy")
controller = IPMFungicideResistanceAntiStrategyEngineController()

@ipm_fungicide_resistance_anti_strategy_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@ipm_fungicide_resistance_anti_strategy_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@ipm_fungicide_resistance_anti_strategy_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
