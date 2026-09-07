"""
GrainDryingPsychrometricEMCEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.grain_drying_psychrometric_emc_controller import GrainDryingPsychrometricEMCEngineController

grain_drying_psychrometric_emc_bp = Blueprint("grain-drying-psychrometric-emc", __name__, url_prefix="/api/grain-drying-psychrometric-emc")
controller = GrainDryingPsychrometricEMCEngineController()

@grain_drying_psychrometric_emc_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@grain_drying_psychrometric_emc_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@grain_drying_psychrometric_emc_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
