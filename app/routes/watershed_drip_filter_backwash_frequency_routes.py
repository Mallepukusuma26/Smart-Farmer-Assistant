"""
WatershedDripFilterBackwashEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.watershed_drip_filter_backwash_frequency_controller import WatershedDripFilterBackwashEngineController

watershed_drip_filter_backwash_frequency_bp = Blueprint("watershed-drip-filter-backwash-frequency", __name__, url_prefix="/api/watershed-drip-filter-backwash-frequency")
controller = WatershedDripFilterBackwashEngineController()

@watershed_drip_filter_backwash_frequency_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@watershed_drip_filter_backwash_frequency_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@watershed_drip_filter_backwash_frequency_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
