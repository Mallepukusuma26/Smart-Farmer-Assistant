"""
IrrigationCenterPivotSpeedDepthEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.irrigation_center_pivot_speed_depth_controller import IrrigationCenterPivotSpeedDepthEngineController

irrigation_center_pivot_speed_depth_bp = Blueprint("irrigation-center-pivot-speed-depth", __name__, url_prefix="/api/irrigation-center-pivot-speed-depth")
controller = IrrigationCenterPivotSpeedDepthEngineController()

@irrigation_center_pivot_speed_depth_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@irrigation_center_pivot_speed_depth_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@irrigation_center_pivot_speed_depth_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
