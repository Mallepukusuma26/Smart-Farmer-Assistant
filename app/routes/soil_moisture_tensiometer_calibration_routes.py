"""
SoilMoistureTensiometerCalibrationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_moisture_tensiometer_calibration_controller import SoilMoistureTensiometerCalibrationEngineController

soil_moisture_tensiometer_calibration_bp = Blueprint("soil-moisture-tensiometer-calibration", __name__, url_prefix="/api/soil-moisture-tensiometer-calibration")
controller = SoilMoistureTensiometerCalibrationEngineController()

@soil_moisture_tensiometer_calibration_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_moisture_tensiometer_calibration_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_moisture_tensiometer_calibration_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
