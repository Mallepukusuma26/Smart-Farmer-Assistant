"""
ClimateCycloneWindLodgingEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.climate_cyclone_wind_lodging_risk_controller import ClimateCycloneWindLodgingEngineController

climate_cyclone_wind_lodging_risk_bp = Blueprint("climate-cyclone-wind-lodging-risk", __name__, url_prefix="/api/climate-cyclone-wind-lodging-risk")
controller = ClimateCycloneWindLodgingEngineController()

@climate_cyclone_wind_lodging_risk_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@climate_cyclone_wind_lodging_risk_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@climate_cyclone_wind_lodging_risk_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
