"""
Fertigation Salt Index & Hydroponic Solubility Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertilizer_fertigation_solubility_controller import FertigationSolubilityEngineController

fertilizer_fertigation_solubility_engine_bp = Blueprint("fertilizer-fertigation-solubility", __name__, url_prefix="/api/fertilizer-fertigation-solubility")
controller = FertigationSolubilityEngineController()

@fertilizer_fertigation_solubility_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@fertilizer_fertigation_solubility_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
