"""
CropEvapotranspirationFAO56PenmanEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_evapotranspiration_fao56_penman_controller import CropEvapotranspirationFAO56PenmanEngineController

crop_evapotranspiration_fao56_penman_bp = Blueprint("crop-evapotranspiration-fao56-penman", __name__, url_prefix="/api/crop-evapotranspiration-fao56-penman")
controller = CropEvapotranspirationFAO56PenmanEngineController()

@crop_evapotranspiration_fao56_penman_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_evapotranspiration_fao56_penman_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_evapotranspiration_fao56_penman_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
