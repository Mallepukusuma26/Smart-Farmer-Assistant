"""
ClimateUnseasonalFrostAlertEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.climate_unseasonal_frost_alert_model_controller import ClimateUnseasonalFrostAlertEngineController

climate_unseasonal_frost_alert_model_bp = Blueprint("climate-unseasonal-frost-alert-model", __name__, url_prefix="/api/climate-unseasonal-frost-alert-model")
controller = ClimateUnseasonalFrostAlertEngineController()

@climate_unseasonal_frost_alert_model_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@climate_unseasonal_frost_alert_model_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@climate_unseasonal_frost_alert_model_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
