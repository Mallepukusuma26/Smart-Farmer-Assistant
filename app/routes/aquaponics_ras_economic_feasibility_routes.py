"""
AquaponicsRASEconomicFeasibilityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.aquaponics_ras_economic_feasibility_controller import AquaponicsRASEconomicFeasibilityEngineController

aquaponics_ras_economic_feasibility_bp = Blueprint("aquaponics-ras-economic-feasibility", __name__, url_prefix="/api/aquaponics-ras-economic-feasibility")
controller = AquaponicsRASEconomicFeasibilityEngineController()

@aquaponics_ras_economic_feasibility_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@aquaponics_ras_economic_feasibility_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@aquaponics_ras_economic_feasibility_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
