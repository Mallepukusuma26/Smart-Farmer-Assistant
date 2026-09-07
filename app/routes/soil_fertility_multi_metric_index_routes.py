"""
SoilFertilityMultiMetricIndexEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_fertility_multi_metric_index_controller import SoilFertilityMultiMetricIndexEngineController

soil_fertility_multi_metric_index_bp = Blueprint("soil-fertility-multi-metric-index", __name__, url_prefix="/api/soil-fertility-multi-metric-index")
controller = SoilFertilityMultiMetricIndexEngineController()

@soil_fertility_multi_metric_index_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_fertility_multi_metric_index_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_fertility_multi_metric_index_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
