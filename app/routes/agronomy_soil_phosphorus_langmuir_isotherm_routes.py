"""
AgronomySoilPhosphorusLangmuirIsothermEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_soil_phosphorus_langmuir_isotherm_controller import AgronomySoilPhosphorusLangmuirIsothermEngineController

agronomy_soil_phosphorus_langmuir_isotherm_bp = Blueprint("agronomy-soil-phosphorus-langmuir-isotherm", __name__, url_prefix="/api/agronomy-soil-phosphorus-langmuir-isotherm")
controller = AgronomySoilPhosphorusLangmuirIsothermEngineController()

@agronomy_soil_phosphorus_langmuir_isotherm_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_soil_phosphorus_langmuir_isotherm_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
