"""
DripEmitterFlowUniformityCUEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.drip_emitter_flow_uniformity_cu_controller import DripEmitterFlowUniformityCUEngineController

drip_emitter_flow_uniformity_cu_bp = Blueprint("drip-emitter-flow-uniformity-cu", __name__, url_prefix="/api/drip-emitter-flow-uniformity-cu")
controller = DripEmitterFlowUniformityCUEngineController()

@drip_emitter_flow_uniformity_cu_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@drip_emitter_flow_uniformity_cu_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@drip_emitter_flow_uniformity_cu_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
