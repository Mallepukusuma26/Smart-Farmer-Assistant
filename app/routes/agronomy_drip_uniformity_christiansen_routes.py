"""
AgronomyDripUniformityChristiansenEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_drip_uniformity_christiansen_controller import AgronomyDripUniformityChristiansenEngineController

agronomy_drip_uniformity_christiansen_bp = Blueprint("agronomy-drip-uniformity-christiansen", __name__, url_prefix="/api/agronomy-drip-uniformity-christiansen")
controller = AgronomyDripUniformityChristiansenEngineController()

@agronomy_drip_uniformity_christiansen_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_drip_uniformity_christiansen_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
