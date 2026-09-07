"""
Drip Emitter Hydraulics & Christiansen Uniformity Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.drip_emitter_flow_uniformity_controller import DripEmitterUniformityEngineController

drip_emitter_flow_uniformity_engine_bp = Blueprint("drip-emitter-flow-uniformity", __name__, url_prefix="/api/drip-emitter-flow-uniformity")
controller = DripEmitterUniformityEngineController()

@drip_emitter_flow_uniformity_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@drip_emitter_flow_uniformity_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
