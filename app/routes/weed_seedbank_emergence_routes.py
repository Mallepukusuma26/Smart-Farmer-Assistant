"""
Weed Seedbank Dynamics & Emergence Timing Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.weed_seedbank_emergence_controller import WeedSeedbankEngineController

weed_seedbank_emergence_engine_bp = Blueprint("weed-seedbank-emergence", __name__, url_prefix="/api/weed-seedbank-emergence")
controller = WeedSeedbankEngineController()

@weed_seedbank_emergence_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@weed_seedbank_emergence_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
