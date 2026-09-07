"""
AgronomyFertilizerFertigationSolubilityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_fertilizer_fertigation_solubility_controller import AgronomyFertilizerFertigationSolubilityEngineController

agronomy_fertilizer_fertigation_solubility_bp = Blueprint("agronomy-fertilizer-fertigation-solubility", __name__, url_prefix="/api/agronomy-fertilizer-fertigation-solubility")
controller = AgronomyFertilizerFertigationSolubilityEngineController()

@agronomy_fertilizer_fertigation_solubility_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_fertilizer_fertigation_solubility_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
