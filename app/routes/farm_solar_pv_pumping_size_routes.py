"""
FarmSolarPVPumpingSizeEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.farm_solar_pv_pumping_size_controller import FarmSolarPVPumpingSizeEngineController

farm_solar_pv_pumping_size_bp = Blueprint("farm-solar-pv-pumping-size", __name__, url_prefix="/api/farm-solar-pv-pumping-size")
controller = FarmSolarPVPumpingSizeEngineController()

@farm_solar_pv_pumping_size_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@farm_solar_pv_pumping_size_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@farm_solar_pv_pumping_size_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
