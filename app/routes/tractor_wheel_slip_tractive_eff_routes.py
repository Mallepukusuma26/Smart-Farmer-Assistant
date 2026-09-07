"""
TractorWheelSlipTractiveEffEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.tractor_wheel_slip_tractive_eff_controller import TractorWheelSlipTractiveEffEngineController

tractor_wheel_slip_tractive_eff_bp = Blueprint("tractor-wheel-slip-tractive-eff", __name__, url_prefix="/api/tractor-wheel-slip-tractive-eff")
controller = TractorWheelSlipTractiveEffEngineController()

@tractor_wheel_slip_tractive_eff_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@tractor_wheel_slip_tractive_eff_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@tractor_wheel_slip_tractive_eff_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
