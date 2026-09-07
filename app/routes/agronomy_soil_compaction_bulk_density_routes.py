"""
AgronomySoilCompactionBulkDensityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_soil_compaction_bulk_density_controller import AgronomySoilCompactionBulkDensityEngineController

agronomy_soil_compaction_bulk_density_bp = Blueprint("agronomy-soil-compaction-bulk-density", __name__, url_prefix="/api/agronomy-soil-compaction-bulk-density")
controller = AgronomySoilCompactionBulkDensityEngineController()

@agronomy_soil_compaction_bulk_density_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_soil_compaction_bulk_density_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
