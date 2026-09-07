"""
AgronomyTillageEnergyRequirementEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_tillage_energy_requirement_controller import AgronomyTillageEnergyRequirementEngineController

agronomy_tillage_energy_requirement_bp = Blueprint("agronomy-tillage-energy-requirement", __name__, url_prefix="/api/agronomy-tillage-energy-requirement")
controller = AgronomyTillageEnergyRequirementEngineController()

@agronomy_tillage_energy_requirement_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_tillage_energy_requirement_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
