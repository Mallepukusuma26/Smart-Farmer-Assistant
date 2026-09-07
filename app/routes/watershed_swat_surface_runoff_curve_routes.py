"""
WatershedSWATSurfaceRunoffCurveEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.watershed_swat_surface_runoff_curve_controller import WatershedSWATSurfaceRunoffCurveEngineController

watershed_swat_surface_runoff_curve_bp = Blueprint("watershed-swat-surface-runoff-curve", __name__, url_prefix="/api/watershed-swat-surface-runoff-curve")
controller = WatershedSWATSurfaceRunoffCurveEngineController()

@watershed_swat_surface_runoff_curve_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@watershed_swat_surface_runoff_curve_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@watershed_swat_surface_runoff_curve_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
