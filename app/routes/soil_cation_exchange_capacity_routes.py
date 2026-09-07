"""
Cation Exchange Capacity (CEC) Base Saturation Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_cation_exchange_capacity_controller import CECBaseSaturationEngineController

soil_cation_exchange_capacity_engine_bp = Blueprint("soil-cation-exchange-capacity", __name__, url_prefix="/api/soil-cation-exchange-capacity")
controller = CECBaseSaturationEngineController()

@soil_cation_exchange_capacity_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@soil_cation_exchange_capacity_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
