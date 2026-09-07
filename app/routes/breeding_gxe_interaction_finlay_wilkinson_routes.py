"""
BreedingGxEInteractionFinlayWilkinsonEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.breeding_gxe_interaction_finlay_wilkinson_controller import BreedingGxEInteractionFinlayWilkinsonEngineController

breeding_gxe_interaction_finlay_wilkinson_bp = Blueprint("breeding-gxe-interaction-finlay-wilkinson", __name__, url_prefix="/api/breeding-gxe-interaction-finlay-wilkinson")
controller = BreedingGxEInteractionFinlayWilkinsonEngineController()

@breeding_gxe_interaction_finlay_wilkinson_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@breeding_gxe_interaction_finlay_wilkinson_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@breeding_gxe_interaction_finlay_wilkinson_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
