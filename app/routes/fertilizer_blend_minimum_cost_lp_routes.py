"""
FertilizerBlendMinimumCostLPEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertilizer_blend_minimum_cost_lp_controller import FertilizerBlendMinimumCostLPEngineController

fertilizer_blend_minimum_cost_lp_bp = Blueprint("fertilizer-blend-minimum-cost-lp", __name__, url_prefix="/api/fertilizer-blend-minimum-cost-lp")
controller = FertilizerBlendMinimumCostLPEngineController()

@fertilizer_blend_minimum_cost_lp_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@fertilizer_blend_minimum_cost_lp_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@fertilizer_blend_minimum_cost_lp_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
