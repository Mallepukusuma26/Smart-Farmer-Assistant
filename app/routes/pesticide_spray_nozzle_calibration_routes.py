"""
PesticideSprayNozzleCalibrationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.pesticide_spray_nozzle_calibration_controller import PesticideSprayNozzleCalibrationEngineController

pesticide_spray_nozzle_calibration_bp = Blueprint("pesticide-spray-nozzle-calibration", __name__, url_prefix="/api/pesticide-spray-nozzle-calibration")
controller = PesticideSprayNozzleCalibrationEngineController()

@pesticide_spray_nozzle_calibration_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@pesticide_spray_nozzle_calibration_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@pesticide_spray_nozzle_calibration_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
