"""
Grain Aeration Cooling & Psychrometric EMC Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.grain_aeration_psychrometric_controller import GrainAerationEngineController

grain_aeration_psychrometric_engine_bp = Blueprint("grain-aeration-psychrometric", __name__, url_prefix="/api/grain-aeration-psychrometric")
controller = GrainAerationEngineController()

@grain_aeration_psychrometric_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@grain_aeration_psychrometric_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
