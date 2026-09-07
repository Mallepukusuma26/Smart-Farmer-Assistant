"""
GreenhouseEnergyBalanceHVACEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.greenhouse_energy_balance_hvac_controller import GreenhouseEnergyBalanceHVACEngineController

greenhouse_energy_balance_hvac_bp = Blueprint("greenhouse-energy-balance-hvac", __name__, url_prefix="/api/greenhouse-energy-balance-hvac")
controller = GreenhouseEnergyBalanceHVACEngineController()

@greenhouse_energy_balance_hvac_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@greenhouse_energy_balance_hvac_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@greenhouse_energy_balance_hvac_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
