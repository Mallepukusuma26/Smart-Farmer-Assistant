"""
AgronomyCropRotationDiseaseBreakEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_crop_rotation_disease_break_controller import AgronomyCropRotationDiseaseBreakEngineController

agronomy_crop_rotation_disease_break_bp = Blueprint("agronomy-crop-rotation-disease-break", __name__, url_prefix="/api/agronomy-crop-rotation-disease-break")
ctrl = AgronomyCropRotationDiseaseBreakEngineController()

@agronomy_crop_rotation_disease_break_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
