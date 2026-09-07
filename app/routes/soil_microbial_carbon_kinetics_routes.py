"""
SoilMicrobialCarbonKineticsEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_microbial_carbon_kinetics_controller import SoilMicrobialCarbonKineticsEngineController

soil_microbial_carbon_kinetics_bp = Blueprint("soil-microbial-carbon-kinetics", __name__, url_prefix="/api/soil-microbial-carbon-kinetics")
controller = SoilMicrobialCarbonKineticsEngineController()

@soil_microbial_carbon_kinetics_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_microbial_carbon_kinetics_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_microbial_carbon_kinetics_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
