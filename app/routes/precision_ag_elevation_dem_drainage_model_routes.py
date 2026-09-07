"""
PrecisionAgElevationDEMDrainageEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_elevation_dem_drainage_model_controller import PrecisionAgElevationDEMDrainageEngineController

precision_ag_elevation_dem_drainage_model_bp = Blueprint("precision-ag-elevation-dem-drainage-model", __name__, url_prefix="/api/precision-ag-elevation-dem-drainage-model")
controller = PrecisionAgElevationDEMDrainageEngineController()

@precision_ag_elevation_dem_drainage_model_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_elevation_dem_drainage_model_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_elevation_dem_drainage_model_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
