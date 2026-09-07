"""
Soil Penetrometer Compaction & Root Penetration Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_compaction_root_growth_controller import SoilCompactionRootEngineController

soil_compaction_root_growth_engine_bp = Blueprint("soil-compaction-root-growth", __name__, url_prefix="/api/soil-compaction-root-growth")
controller = SoilCompactionRootEngineController()

@soil_compaction_root_growth_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@soil_compaction_root_growth_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
