"""
LivestockSilvopastureGrazingCapacityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.livestock_silvopasture_grazing_capacity_controller import LivestockSilvopastureGrazingCapacityEngineController

livestock_silvopasture_grazing_capacity_bp = Blueprint("livestock-silvopasture-grazing-capacity", __name__, url_prefix="/api/livestock-silvopasture-grazing-capacity")
controller = LivestockSilvopastureGrazingCapacityEngineController()

@livestock_silvopasture_grazing_capacity_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@livestock_silvopasture_grazing_capacity_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@livestock_silvopasture_grazing_capacity_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
