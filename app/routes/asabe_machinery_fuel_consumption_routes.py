"""
ASABEMachineryFuelConsumptionEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.asabe_machinery_fuel_consumption_controller import ASABEMachineryFuelConsumptionEngineController

asabe_machinery_fuel_consumption_bp = Blueprint("asabe-machinery-fuel-consumption", __name__, url_prefix="/api/asabe-machinery-fuel-consumption")
controller = ASABEMachineryFuelConsumptionEngineController()

@asabe_machinery_fuel_consumption_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@asabe_machinery_fuel_consumption_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@asabe_machinery_fuel_consumption_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
