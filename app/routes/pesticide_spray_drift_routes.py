"""
Droplet Size & Wind Spray Drift Deposition Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.pesticide_spray_drift_controller import SprayDriftDepositionEngineController

pesticide_spray_drift_engine_bp = Blueprint("pesticide-spray-drift", __name__, url_prefix="/api/pesticide-spray-drift")
controller = SprayDriftDepositionEngineController()

@pesticide_spray_drift_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@pesticide_spray_drift_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
