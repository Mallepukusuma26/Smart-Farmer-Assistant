"""
SoilNitrogenMineralizationKineticsEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_nitrogen_mineralization_kinetics_controller import SoilNitrogenMineralizationKineticsEngineController

soil_nitrogen_mineralization_kinetics_bp = Blueprint("soil-nitrogen-mineralization-kinetics", __name__, url_prefix="/api/soil-nitrogen-mineralization-kinetics")
controller = SoilNitrogenMineralizationKineticsEngineController()

@soil_nitrogen_mineralization_kinetics_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_nitrogen_mineralization_kinetics_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_nitrogen_mineralization_kinetics_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
