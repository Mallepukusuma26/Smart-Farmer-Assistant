"""
ASABETractorPowerDraftForceEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.asabe_tractor_power_draft_force_controller import ASABETractorPowerDraftForceEngineController

asabe_tractor_power_draft_force_bp = Blueprint("asabe-tractor-power-draft-force", __name__, url_prefix="/api/asabe-tractor-power-draft-force")
controller = ASABETractorPowerDraftForceEngineController()

@asabe_tractor_power_draft_force_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@asabe_tractor_power_draft_force_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@asabe_tractor_power_draft_force_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
