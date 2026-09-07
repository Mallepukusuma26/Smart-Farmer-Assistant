"""
AgronomyGrainDryingPsychrometricEMCEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_grain_drying_psychrometric_emc_controller import AgronomyGrainDryingPsychrometricEMCEngineController

agronomy_grain_drying_psychrometric_emc_bp = Blueprint("agronomy-grain-drying-psychrometric-emc", __name__, url_prefix="/api/agronomy-grain-drying-psychrometric-emc")
controller = AgronomyGrainDryingPsychrometricEMCEngineController()

@agronomy_grain_drying_psychrometric_emc_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_grain_drying_psychrometric_emc_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
