"""
Organic Compost Thermophilic Phase Kinetics Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.compost_thermal_kinetics_controller import CompostKineticsEngineController

compost_thermal_kinetics_engine_bp = Blueprint("compost-thermal-kinetics", __name__, url_prefix="/api/compost-thermal-kinetics")
controller = CompostKineticsEngineController()

@compost_thermal_kinetics_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@compost_thermal_kinetics_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
