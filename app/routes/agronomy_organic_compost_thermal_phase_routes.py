"""
AgronomyOrganicCompostThermalPhaseEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_organic_compost_thermal_phase_controller import AgronomyOrganicCompostThermalPhaseEngineController

agronomy_organic_compost_thermal_phase_bp = Blueprint("agronomy-organic-compost-thermal-phase", __name__, url_prefix="/api/agronomy-organic-compost-thermal-phase")
controller = AgronomyOrganicCompostThermalPhaseEngineController()

@agronomy_organic_compost_thermal_phase_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_organic_compost_thermal_phase_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
