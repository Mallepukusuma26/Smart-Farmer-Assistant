"""
AgronomyCropHeatUnitAccumulationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_crop_heat_unit_accumulation_controller import AgronomyCropHeatUnitAccumulationEngineController

agronomy_crop_heat_unit_accumulation_bp = Blueprint("agronomy-crop-heat-unit-accumulation", __name__, url_prefix="/api/agronomy-crop-heat-unit-accumulation")
controller = AgronomyCropHeatUnitAccumulationEngineController()

@agronomy_crop_heat_unit_accumulation_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_crop_heat_unit_accumulation_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
