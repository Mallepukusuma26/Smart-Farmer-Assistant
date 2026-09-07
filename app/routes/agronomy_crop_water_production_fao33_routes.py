"""
AgronomyCropWaterProductionFAO33Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_crop_water_production_fao33_controller import AgronomyCropWaterProductionFAO33EngineController

agronomy_crop_water_production_fao33_bp = Blueprint("agronomy-crop-water-production-fao33", __name__, url_prefix="/api/agronomy-crop-water-production-fao33")
controller = AgronomyCropWaterProductionFAO33EngineController()

@agronomy_crop_water_production_fao33_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_crop_water_production_fao33_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
