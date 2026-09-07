"""
AgronomyRUSLE2ErosionToleranceEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_rusle2_erosion_tolerance_controller import AgronomyRUSLE2ErosionToleranceEngineController

agronomy_rusle2_erosion_tolerance_bp = Blueprint("agronomy-rusle2-erosion-tolerance", __name__, url_prefix="/api/agronomy-rusle2-erosion-tolerance")
controller = AgronomyRUSLE2ErosionToleranceEngineController()

@agronomy_rusle2_erosion_tolerance_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_rusle2_erosion_tolerance_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
