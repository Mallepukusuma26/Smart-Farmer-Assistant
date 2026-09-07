"""
BreedingMarkerAssistedSelectionQTLEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.breeding_marker_assisted_selection_qtl_controller import BreedingMarkerAssistedSelectionQTLEngineController

breeding_marker_assisted_selection_qtl_bp = Blueprint("breeding-marker-assisted-selection-qtl", __name__, url_prefix="/api/breeding-marker-assisted-selection-qtl")
controller = BreedingMarkerAssistedSelectionQTLEngineController()

@breeding_marker_assisted_selection_qtl_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@breeding_marker_assisted_selection_qtl_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@breeding_marker_assisted_selection_qtl_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
