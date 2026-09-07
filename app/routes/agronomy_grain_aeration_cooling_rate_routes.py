"""
AgronomyGrainAerationCoolingRateEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_grain_aeration_cooling_rate_controller import AgronomyGrainAerationCoolingRateEngineController

agronomy_grain_aeration_cooling_rate_bp = Blueprint("agronomy-grain-aeration-cooling-rate", __name__, url_prefix="/api/agronomy-grain-aeration-cooling-rate")
ctrl = AgronomyGrainAerationCoolingRateEngineController()

@agronomy_grain_aeration_cooling_rate_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
