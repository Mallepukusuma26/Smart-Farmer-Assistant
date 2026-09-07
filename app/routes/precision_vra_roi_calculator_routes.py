"""
PrecisionVRAROICalculatorEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_vra_roi_calculator_controller import PrecisionVRAROICalculatorEngineController

precision_vra_roi_calculator_bp = Blueprint("precision-vra-roi-calculator", __name__, url_prefix="/api/precision-vra-roi-calculator")
controller = PrecisionVRAROICalculatorEngineController()

@precision_vra_roi_calculator_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@precision_vra_roi_calculator_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@precision_vra_roi_calculator_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
