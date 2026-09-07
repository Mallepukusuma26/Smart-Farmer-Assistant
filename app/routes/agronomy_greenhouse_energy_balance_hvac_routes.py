"""
AgronomyGreenhouseEnergyBalanceHVACEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_greenhouse_energy_balance_hvac_controller import AgronomyGreenhouseEnergyBalanceHVACEngineController

agronomy_greenhouse_energy_balance_hvac_bp = Blueprint("agronomy-greenhouse-energy-balance-hvac", __name__, url_prefix="/api/agronomy-greenhouse-energy-balance-hvac")
controller = AgronomyGreenhouseEnergyBalanceHVACEngineController()

@agronomy_greenhouse_energy_balance_hvac_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_greenhouse_energy_balance_hvac_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
