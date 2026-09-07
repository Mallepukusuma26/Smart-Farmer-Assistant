"""
AgronomyDripEmitterCloggingRiskEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_drip_emitter_clogging_risk_controller import AgronomyDripEmitterCloggingRiskEngineController

agronomy_drip_emitter_clogging_risk_bp = Blueprint("agronomy-drip-emitter-clogging-risk", __name__, url_prefix="/api/agronomy-drip-emitter-clogging-risk")
controller = AgronomyDripEmitterCloggingRiskEngineController()

@agronomy_drip_emitter_clogging_risk_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_drip_emitter_clogging_risk_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
