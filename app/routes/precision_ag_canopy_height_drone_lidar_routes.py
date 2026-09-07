"""
PrecisionAgCanopyHeightDroneLidarEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_canopy_height_drone_lidar_controller import PrecisionAgCanopyHeightDroneLidarEngineController

precision_ag_canopy_height_drone_lidar_bp = Blueprint("precision-ag-canopy-height-drone-lidar", __name__, url_prefix="/api/precision-ag-canopy-height-drone-lidar")
controller = PrecisionAgCanopyHeightDroneLidarEngineController()

@precision_ag_canopy_height_drone_lidar_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_canopy_height_drone_lidar_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_canopy_height_drone_lidar_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
