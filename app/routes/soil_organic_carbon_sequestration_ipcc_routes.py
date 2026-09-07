"""
SoilOrganicCarbonSequestrationIPCCEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_organic_carbon_sequestration_ipcc_controller import SoilOrganicCarbonSequestrationIPCCEngineController

soil_organic_carbon_sequestration_ipcc_bp = Blueprint("soil-organic-carbon-sequestration-ipcc", __name__, url_prefix="/api/soil-organic-carbon-sequestration-ipcc")
controller = SoilOrganicCarbonSequestrationIPCCEngineController()

@soil_organic_carbon_sequestration_ipcc_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_organic_carbon_sequestration_ipcc_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_organic_carbon_sequestration_ipcc_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
