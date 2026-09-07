"""
WatershedFarmPondHarvestingCapacityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.watershed_farm_pond_harvesting_capacity_controller import WatershedFarmPondHarvestingCapacityEngineController

watershed_farm_pond_harvesting_capacity_bp = Blueprint("watershed-farm-pond-harvesting-capacity", __name__, url_prefix="/api/watershed-farm-pond-harvesting-capacity")
controller = WatershedFarmPondHarvestingCapacityEngineController()

@watershed_farm_pond_harvesting_capacity_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@watershed_farm_pond_harvesting_capacity_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@watershed_farm_pond_harvesting_capacity_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
