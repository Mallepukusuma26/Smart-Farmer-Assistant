"""
AgronomyGreenhouseMicroclimateVPDEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_greenhouse_microclimate_vpd_controller import AgronomyGreenhouseMicroclimateVPDEngineController

agronomy_greenhouse_microclimate_vpd_bp = Blueprint("agronomy-greenhouse-microclimate-vpd", __name__, url_prefix="/api/agronomy-greenhouse-microclimate-vpd")
ctrl = AgronomyGreenhouseMicroclimateVPDEngineController()

@agronomy_greenhouse_microclimate_vpd_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
