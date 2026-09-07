"""
PrecisionAgNitrogenResponseCurveEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_nitrogen_response_curve_model_controller import PrecisionAgNitrogenResponseCurveEngineController

precision_ag_nitrogen_response_curve_model_bp = Blueprint("precision-ag-nitrogen-response-curve-model", __name__, url_prefix="/api/precision-ag-nitrogen-response-curve-model")
controller = PrecisionAgNitrogenResponseCurveEngineController()

@precision_ag_nitrogen_response_curve_model_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_nitrogen_response_curve_model_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_nitrogen_response_curve_model_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
