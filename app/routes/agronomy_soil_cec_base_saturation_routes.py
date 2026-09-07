"""
AgronomySoilCECBaseSaturationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_soil_cec_base_saturation_controller import AgronomySoilCECBaseSaturationEngineController

agronomy_soil_cec_base_saturation_bp = Blueprint("agronomy-soil-cec-base-saturation", __name__, url_prefix="/api/agronomy-soil-cec-base-saturation")
controller = AgronomySoilCECBaseSaturationEngineController()

@agronomy_soil_cec_base_saturation_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_soil_cec_base_saturation_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
