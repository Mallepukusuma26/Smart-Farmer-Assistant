"""
IPCC Tier 2 Soil Organic Carbon Sequestration Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.carbon_sequestration_ipcc_controller import IPCCSoilCarbonEngineController

carbon_sequestration_ipcc_engine_bp = Blueprint("carbon-sequestration-ipcc", __name__, url_prefix="/api/carbon-sequestration-ipcc")
controller = IPCCSoilCarbonEngineController()

@carbon_sequestration_ipcc_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@carbon_sequestration_ipcc_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
