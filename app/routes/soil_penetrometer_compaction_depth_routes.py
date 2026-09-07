"""
SoilPenetrometerCompactionDepthEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_penetrometer_compaction_depth_controller import SoilPenetrometerCompactionDepthEngineController

soil_penetrometer_compaction_depth_bp = Blueprint("soil-penetrometer-compaction-depth", __name__, url_prefix="/api/soil-penetrometer-compaction-depth")
controller = SoilPenetrometerCompactionDepthEngineController()

@soil_penetrometer_compaction_depth_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_penetrometer_compaction_depth_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_penetrometer_compaction_depth_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
