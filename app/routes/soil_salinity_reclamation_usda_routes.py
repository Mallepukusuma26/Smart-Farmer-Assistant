"""
SoilSalinityReclamationUSDAEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_salinity_reclamation_usda_controller import SoilSalinityReclamationUSDAEngineController

soil_salinity_reclamation_usda_bp = Blueprint("soil-salinity-reclamation-usda", __name__, url_prefix="/api/soil-salinity-reclamation-usda")
controller = SoilSalinityReclamationUSDAEngineController()

@soil_salinity_reclamation_usda_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_salinity_reclamation_usda_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_salinity_reclamation_usda_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
