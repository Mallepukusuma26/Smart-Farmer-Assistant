"""
CropDiseaseSIREpidemiologyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_disease_sir_epidemiology_controller import CropDiseaseSIREpidemiologyEngineController

crop_disease_sir_epidemiology_bp = Blueprint("crop-disease-sir-epidemiology", __name__, url_prefix="/api/crop-disease-sir-epidemiology")
controller = CropDiseaseSIREpidemiologyEngineController()

@crop_disease_sir_epidemiology_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_disease_sir_epidemiology_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_disease_sir_epidemiology_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
