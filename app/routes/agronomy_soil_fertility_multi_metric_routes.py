"""
AgronomySoilFertilityMultiMetricEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_soil_fertility_multi_metric_controller import AgronomySoilFertilityMultiMetricEngineController

agronomy_soil_fertility_multi_metric_bp = Blueprint("agronomy-soil-fertility-multi-metric", __name__, url_prefix="/api/agronomy-soil-fertility-multi-metric")
controller = AgronomySoilFertilityMultiMetricEngineController()

@agronomy_soil_fertility_multi_metric_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_soil_fertility_multi_metric_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
