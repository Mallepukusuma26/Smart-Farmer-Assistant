"""
Dual Crop Coefficient FAO-56 Transpiration Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_evapotranspiration_dual_kc_controller import DualKcEvapotranspirationEngineController

crop_evapotranspiration_dual_kc_engine_bp = Blueprint("crop-evapotranspiration-dual-kc", __name__, url_prefix="/api/crop-evapotranspiration-dual-kc")
controller = DualKcEvapotranspirationEngineController()

@crop_evapotranspiration_dual_kc_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@crop_evapotranspiration_dual_kc_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
