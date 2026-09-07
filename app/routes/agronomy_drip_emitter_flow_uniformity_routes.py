"""
AgronomyDripEmitterFlowUniformityEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_drip_emitter_flow_uniformity_controller import AgronomyDripEmitterFlowUniformityEngineController

agronomy_drip_emitter_flow_uniformity_bp = Blueprint("agronomy-drip-emitter-flow-uniformity", __name__, url_prefix="/api/agronomy-drip-emitter-flow-uniformity")
ctrl = AgronomyDripEmitterFlowUniformityEngineController()

@agronomy_drip_emitter_flow_uniformity_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
