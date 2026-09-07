"""
ASABE Tractor Power Draft & Fuel Rate Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.asabe_tractor_power_draft_controller import ASABETractorPowerEngineController

asabe_tractor_power_draft_engine_bp = Blueprint("asabe-tractor-power-draft", __name__, url_prefix="/api/asabe-tractor-power-draft")
controller = ASABETractorPowerEngineController()

@asabe_tractor_power_draft_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@asabe_tractor_power_draft_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
