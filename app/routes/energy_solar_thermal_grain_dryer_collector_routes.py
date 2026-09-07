"""
EnergySolarThermalGrainDryerCollectorEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.energy_solar_thermal_grain_dryer_collector_controller import EnergySolarThermalGrainDryerCollectorEngineController

energy_solar_thermal_grain_dryer_collector_bp = Blueprint("energy-solar-thermal-grain-dryer-collector", __name__, url_prefix="/api/energy-solar-thermal-grain-dryer-collector")
controller = EnergySolarThermalGrainDryerCollectorEngineController()

@energy_solar_thermal_grain_dryer_collector_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@energy_solar_thermal_grain_dryer_collector_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@energy_solar_thermal_grain_dryer_collector_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
