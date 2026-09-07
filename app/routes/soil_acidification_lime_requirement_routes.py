"""
SoilAcidificationLimeRequirementEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_acidification_lime_requirement_controller import SoilAcidificationLimeRequirementEngineController

soil_acidification_lime_requirement_bp = Blueprint("soil-acidification-lime-requirement", __name__, url_prefix="/api/soil-acidification-lime-requirement")
controller = SoilAcidificationLimeRequirementEngineController()

@soil_acidification_lime_requirement_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_acidification_lime_requirement_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_acidification_lime_requirement_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
