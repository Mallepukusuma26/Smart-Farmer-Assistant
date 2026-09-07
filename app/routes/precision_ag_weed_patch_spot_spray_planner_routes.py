"""
PrecisionAgWeedPatchSpotSprayEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_weed_patch_spot_spray_planner_controller import PrecisionAgWeedPatchSpotSprayEngineController

precision_ag_weed_patch_spot_spray_planner_bp = Blueprint("precision-ag-weed-patch-spot-spray-planner", __name__, url_prefix="/api/precision-ag-weed-patch-spot-spray-planner")
controller = PrecisionAgWeedPatchSpotSprayEngineController()

@precision_ag_weed_patch_spot_spray_planner_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_weed_patch_spot_spray_planner_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_weed_patch_spot_spray_planner_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
