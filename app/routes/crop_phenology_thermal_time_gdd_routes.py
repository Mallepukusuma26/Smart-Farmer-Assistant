"""
CropPhenologyThermalTimeGDDEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_phenology_thermal_time_gdd_controller import CropPhenologyThermalTimeGDDEngineController

crop_phenology_thermal_time_gdd_bp = Blueprint("crop-phenology-thermal-time-gdd", __name__, url_prefix="/api/crop-phenology-thermal-time-gdd")
controller = CropPhenologyThermalTimeGDDEngineController()

@crop_phenology_thermal_time_gdd_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_phenology_thermal_time_gdd_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_phenology_thermal_time_gdd_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
