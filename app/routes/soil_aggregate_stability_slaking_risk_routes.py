"""
SoilAggregateStabilitySlakingEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_aggregate_stability_slaking_risk_controller import SoilAggregateStabilitySlakingEngineController

soil_aggregate_stability_slaking_risk_bp = Blueprint("soil-aggregate-stability-slaking-risk", __name__, url_prefix="/api/soil-aggregate-stability-slaking-risk")
controller = SoilAggregateStabilitySlakingEngineController()

@soil_aggregate_stability_slaking_risk_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@soil_aggregate_stability_slaking_risk_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@soil_aggregate_stability_slaking_risk_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
