"""
Irrigation Pump Curve & Friction Loss Hydraulics Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.irrigation_pump_hydraulics_controller import PumpHydraulicsEngineController

irrigation_pump_hydraulics_engine_bp = Blueprint("irrigation-pump-hydraulics", __name__, url_prefix="/api/irrigation-pump-hydraulics")
controller = PumpHydraulicsEngineController()

@irrigation_pump_hydraulics_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@irrigation_pump_hydraulics_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
