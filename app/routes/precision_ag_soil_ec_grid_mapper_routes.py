"""
PrecisionAgSoilECGridMapperEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_soil_ec_grid_mapper_controller import PrecisionAgSoilECGridMapperEngineController

precision_ag_soil_ec_grid_mapper_bp = Blueprint("precision-ag-soil-ec-grid-mapper", __name__, url_prefix="/api/precision-ag-soil-ec-grid-mapper")
controller = PrecisionAgSoilECGridMapperEngineController()

@precision_ag_soil_ec_grid_mapper_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_soil_ec_grid_mapper_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_soil_ec_grid_mapper_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
