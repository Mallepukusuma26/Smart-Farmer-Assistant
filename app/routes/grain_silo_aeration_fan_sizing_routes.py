"""
GrainSiloAerationFanSizingEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.grain_silo_aeration_fan_sizing_controller import GrainSiloAerationFanSizingEngineController

grain_silo_aeration_fan_sizing_bp = Blueprint("grain-silo-aeration-fan-sizing", __name__, url_prefix="/api/grain-silo-aeration-fan-sizing")
controller = GrainSiloAerationFanSizingEngineController()

@grain_silo_aeration_fan_sizing_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@grain_silo_aeration_fan_sizing_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@grain_silo_aeration_fan_sizing_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
