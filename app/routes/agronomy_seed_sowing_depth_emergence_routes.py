"""
AgronomySeedSowingDepthEmergenceEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_seed_sowing_depth_emergence_controller import AgronomySeedSowingDepthEmergenceEngineController

agronomy_seed_sowing_depth_emergence_bp = Blueprint("agronomy-seed-sowing-depth-emergence", __name__, url_prefix="/api/agronomy-seed-sowing-depth-emergence")
ctrl = AgronomySeedSowingDepthEmergenceEngineController()

@agronomy_seed_sowing_depth_emergence_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
