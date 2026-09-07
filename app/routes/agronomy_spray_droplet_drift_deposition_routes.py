"""
AgronomySprayDropletDriftDepositionEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_spray_droplet_drift_deposition_controller import AgronomySprayDropletDriftDepositionEngineController

agronomy_spray_droplet_drift_deposition_bp = Blueprint("agronomy-spray-droplet-drift-deposition", __name__, url_prefix="/api/agronomy-spray-droplet-drift-deposition")
controller = AgronomySprayDropletDriftDepositionEngineController()

@agronomy_spray_droplet_drift_deposition_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_spray_droplet_drift_deposition_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
