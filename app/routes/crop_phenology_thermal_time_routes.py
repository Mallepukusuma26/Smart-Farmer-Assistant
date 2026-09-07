"""
Thermal Time & Phenology Stage Transition Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_phenology_thermal_time_controller import ThermalTimePhenologyEngineController

crop_phenology_thermal_time_engine_bp = Blueprint("crop-phenology-thermal-time", __name__, url_prefix="/api/crop-phenology-thermal-time")
controller = ThermalTimePhenologyEngineController()

@crop_phenology_thermal_time_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@crop_phenology_thermal_time_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
