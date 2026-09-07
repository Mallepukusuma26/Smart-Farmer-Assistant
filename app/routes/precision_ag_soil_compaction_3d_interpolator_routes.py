"""
PrecisionAgSoilCompaction3DInterpolatorEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_soil_compaction_3d_interpolator_controller import PrecisionAgSoilCompaction3DInterpolatorEngineController

precision_ag_soil_compaction_3d_interpolator_bp = Blueprint("precision-ag-soil-compaction-3d-interpolator", __name__, url_prefix="/api/precision-ag-soil-compaction-3d-interpolator")
controller = PrecisionAgSoilCompaction3DInterpolatorEngineController()

@precision_ag_soil_compaction_3d_interpolator_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_soil_compaction_3d_interpolator_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_soil_compaction_3d_interpolator_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
