"""
AgronomyFarmMachineryOperatingCostEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_farm_machinery_operating_cost_controller import AgronomyFarmMachineryOperatingCostEngineController

agronomy_farm_machinery_operating_cost_bp = Blueprint("agronomy-farm-machinery-operating-cost", __name__, url_prefix="/api/agronomy-farm-machinery-operating-cost")
ctrl = AgronomyFarmMachineryOperatingCostEngineController()

@agronomy_farm_machinery_operating_cost_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
