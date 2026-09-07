"""
PrecisionFertilizerSpreaderCalEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_fertilizer_spreader_cal_controller import PrecisionFertilizerSpreaderCalEngineController

precision_fertilizer_spreader_cal_bp = Blueprint("precision-fertilizer-spreader-cal", __name__, url_prefix="/api/precision-fertilizer-spreader-cal")
controller = PrecisionFertilizerSpreaderCalEngineController()

@precision_fertilizer_spreader_cal_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@precision_fertilizer_spreader_cal_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@precision_fertilizer_spreader_cal_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
