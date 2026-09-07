"""
LivestockForageDryMatterDemandEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.livestock_forage_dry_matter_demand_controller import LivestockForageDryMatterDemandEngineController

livestock_forage_dry_matter_demand_bp = Blueprint("livestock-forage-dry-matter-demand", __name__, url_prefix="/api/livestock-forage-dry-matter-demand")
controller = LivestockForageDryMatterDemandEngineController()

@livestock_forage_dry_matter_demand_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@livestock_forage_dry_matter_demand_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@livestock_forage_dry_matter_demand_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
