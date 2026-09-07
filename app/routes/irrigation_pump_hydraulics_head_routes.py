"""
IrrigationPumpHydraulicsHeadEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.irrigation_pump_hydraulics_head_controller import IrrigationPumpHydraulicsHeadEngineController

irrigation_pump_hydraulics_head_bp = Blueprint("irrigation-pump-hydraulics-head", __name__, url_prefix="/api/irrigation-pump-hydraulics-head")
controller = IrrigationPumpHydraulicsHeadEngineController()

@irrigation_pump_hydraulics_head_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@irrigation_pump_hydraulics_head_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@irrigation_pump_hydraulics_head_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
