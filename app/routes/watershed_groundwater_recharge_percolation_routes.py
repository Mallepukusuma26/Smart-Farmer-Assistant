"""
WatershedGroundwaterRechargeEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.watershed_groundwater_recharge_percolation_controller import WatershedGroundwaterRechargeEngineController

watershed_groundwater_recharge_percolation_bp = Blueprint("watershed-groundwater-recharge-percolation", __name__, url_prefix="/api/watershed-groundwater-recharge-percolation")
controller = WatershedGroundwaterRechargeEngineController()

@watershed_groundwater_recharge_percolation_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@watershed_groundwater_recharge_percolation_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@watershed_groundwater_recharge_percolation_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
