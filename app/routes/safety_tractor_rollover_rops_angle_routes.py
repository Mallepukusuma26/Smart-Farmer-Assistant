"""
SafetyTractorRolloverROPSAngleEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.safety_tractor_rollover_rops_angle_controller import SafetyTractorRolloverROPSAngleEngineController

safety_tractor_rollover_rops_angle_bp = Blueprint("safety-tractor-rollover-rops-angle", __name__, url_prefix="/api/safety-tractor-rollover-rops-angle")
controller = SafetyTractorRolloverROPSAngleEngineController()

@safety_tractor_rollover_rops_angle_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@safety_tractor_rollover_rops_angle_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@safety_tractor_rollover_rops_angle_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
