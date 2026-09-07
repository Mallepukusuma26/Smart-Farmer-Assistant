"""
AgronomySoilSalinityLeachingFractionEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_soil_salinity_leaching_fraction_controller import AgronomySoilSalinityLeachingFractionEngineController

agronomy_soil_salinity_leaching_fraction_bp = Blueprint("agronomy-soil-salinity-leaching-fraction", __name__, url_prefix="/api/agronomy-soil-salinity-leaching-fraction")
ctrl = AgronomySoilSalinityLeachingFractionEngineController()

@agronomy_soil_salinity_leaching_fraction_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
