"""
AgronomyCropRotationDepletionPenaltyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_crop_rotation_depletion_penalty_controller import AgronomyCropRotationDepletionPenaltyEngineController

agronomy_crop_rotation_depletion_penalty_bp = Blueprint("agronomy-crop-rotation-depletion-penalty", __name__, url_prefix="/api/agronomy-crop-rotation-depletion-penalty")
controller = AgronomyCropRotationDepletionPenaltyEngineController()

@agronomy_crop_rotation_depletion_penalty_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_crop_rotation_depletion_penalty_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
