"""
CEAOrchardCanopyPruningSunlightEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.cea_orchard_canopy_pruning_sunlight_controller import CEAOrchardCanopyPruningSunlightEngineController

cea_orchard_canopy_pruning_sunlight_bp = Blueprint("cea-orchard-canopy-pruning-sunlight", __name__, url_prefix="/api/cea-orchard-canopy-pruning-sunlight")
controller = CEAOrchardCanopyPruningSunlightEngineController()

@cea_orchard_canopy_pruning_sunlight_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@cea_orchard_canopy_pruning_sunlight_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@cea_orchard_canopy_pruning_sunlight_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
