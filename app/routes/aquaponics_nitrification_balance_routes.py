"""
Aquaponics Biofilter TAN & Nitrate Balance Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.aquaponics_nitrification_balance_controller import AquaponicsNitrificationEngineController

aquaponics_nitrification_balance_engine_bp = Blueprint("aquaponics-nitrification-balance", __name__, url_prefix="/api/aquaponics-nitrification-balance")
controller = AquaponicsNitrificationEngineController()

@aquaponics_nitrification_balance_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@aquaponics_nitrification_balance_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
