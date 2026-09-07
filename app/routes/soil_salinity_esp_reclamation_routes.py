"""
Soil Salinity ECe & ESP Gypsum Reclamation Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_salinity_esp_reclamation_controller import SoilSalinityReclamationEngineController

soil_salinity_esp_reclamation_engine_bp = Blueprint("soil-salinity-esp-reclamation", __name__, url_prefix="/api/soil-salinity-esp-reclamation")
controller = SoilSalinityReclamationEngineController()

@soil_salinity_esp_reclamation_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@soil_salinity_esp_reclamation_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
