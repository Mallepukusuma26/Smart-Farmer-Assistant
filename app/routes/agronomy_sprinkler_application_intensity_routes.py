"""
AgronomySprinklerApplicationIntensityEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_sprinkler_application_intensity_controller import AgronomySprinklerApplicationIntensityEngineController

agronomy_sprinkler_application_intensity_bp = Blueprint("agronomy-sprinkler-application-intensity", __name__, url_prefix="/api/agronomy-sprinkler-application-intensity")
ctrl = AgronomySprinklerApplicationIntensityEngineController()

@agronomy_sprinkler_application_intensity_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
