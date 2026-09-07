"""
AgronomySoilErosionRUSLEKFactorEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_soil_erosion_rusle_k_factor_controller import AgronomySoilErosionRUSLEKFactorEngineController

agronomy_soil_erosion_rusle_k_factor_bp = Blueprint("agronomy-soil-erosion-rusle-k-factor", __name__, url_prefix="/api/agronomy-soil-erosion-rusle-k-factor")
ctrl = AgronomySoilErosionRUSLEKFactorEngineController()

@agronomy_soil_erosion_rusle_k_factor_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
