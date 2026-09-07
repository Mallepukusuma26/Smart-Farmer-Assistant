"""
SoilPhosphorusSorptionLangmuirEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_phosphorus_sorption_langmuir_controller import SoilPhosphorusSorptionLangmuirEngineController

soil_phosphorus_sorption_langmuir_bp = Blueprint("soil-phosphorus-sorption-langmuir", __name__, url_prefix="/api/soil-phosphorus-sorption-langmuir")
controller = SoilPhosphorusSorptionLangmuirEngineController()

@soil_phosphorus_sorption_langmuir_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_phosphorus_sorption_langmuir_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_phosphorus_sorption_langmuir_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
