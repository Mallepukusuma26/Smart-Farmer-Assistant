"""
EnergyWindTurbineWaterPumpingPowerEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.energy_wind_turbine_water_pumping_power_controller import EnergyWindTurbineWaterPumpingPowerEngineController

energy_wind_turbine_water_pumping_power_bp = Blueprint("energy-wind-turbine-water-pumping-power", __name__, url_prefix="/api/energy-wind-turbine-water-pumping-power")
controller = EnergyWindTurbineWaterPumpingPowerEngineController()

@energy_wind_turbine_water_pumping_power_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@energy_wind_turbine_water_pumping_power_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@energy_wind_turbine_water_pumping_power_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
