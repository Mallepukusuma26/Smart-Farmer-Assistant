"""
AgronomyIPCCTier2SoilCarbonEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_ipcc_tier2_soil_carbon_controller import AgronomyIPCCTier2SoilCarbonEngineController

agronomy_ipcc_tier2_soil_carbon_bp = Blueprint("agronomy-ipcc-tier2-soil-carbon", __name__, url_prefix="/api/agronomy-ipcc-tier2-soil-carbon")
controller = AgronomyIPCCTier2SoilCarbonEngineController()

@agronomy_ipcc_tier2_soil_carbon_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_ipcc_tier2_soil_carbon_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
