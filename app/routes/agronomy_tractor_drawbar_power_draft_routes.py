"""
AgronomyTractorDrawbarPowerDraftEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_tractor_drawbar_power_draft_controller import AgronomyTractorDrawbarPowerDraftEngineController

agronomy_tractor_drawbar_power_draft_bp = Blueprint("agronomy-tractor-drawbar-power-draft", __name__, url_prefix="/api/agronomy-tractor-drawbar-power-draft")
ctrl = AgronomyTractorDrawbarPowerDraftEngineController()

@agronomy_tractor_drawbar_power_draft_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
