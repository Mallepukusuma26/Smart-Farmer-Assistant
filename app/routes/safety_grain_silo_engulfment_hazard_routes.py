"""
SafetyGrainSiloEngulfmentHazardEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.safety_grain_silo_engulfment_hazard_controller import SafetyGrainSiloEngulfmentHazardEngineController

safety_grain_silo_engulfment_hazard_bp = Blueprint("safety-grain-silo-engulfment-hazard", __name__, url_prefix="/api/safety-grain-silo-engulfment-hazard")
controller = SafetyGrainSiloEngulfmentHazardEngineController()

@safety_grain_silo_engulfment_hazard_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@safety_grain_silo_engulfment_hazard_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@safety_grain_silo_engulfment_hazard_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
