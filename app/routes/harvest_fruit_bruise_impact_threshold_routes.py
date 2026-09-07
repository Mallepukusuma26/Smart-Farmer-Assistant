"""
HarvestFruitBruiseImpactThresholdEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.harvest_fruit_bruise_impact_threshold_controller import HarvestFruitBruiseImpactThresholdEngineController

harvest_fruit_bruise_impact_threshold_bp = Blueprint("harvest-fruit-bruise-impact-threshold", __name__, url_prefix="/api/harvest-fruit-bruise-impact-threshold")
controller = HarvestFruitBruiseImpactThresholdEngineController()

@harvest_fruit_bruise_impact_threshold_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@harvest_fruit_bruise_impact_threshold_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@harvest_fruit_bruise_impact_threshold_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
