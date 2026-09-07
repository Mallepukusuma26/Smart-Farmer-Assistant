"""
AgronomyCropCanopyArchitecture3DEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_crop_canopy_architecture_3d_controller import AgronomyCropCanopyArchitecture3DEngineController

agronomy_crop_canopy_architecture_3d_bp = Blueprint("agronomy-crop-canopy-architecture-3d", __name__, url_prefix="/api/agronomy-crop-canopy-architecture-3d")
ctrl = AgronomyCropCanopyArchitecture3DEngineController()

@agronomy_crop_canopy_architecture_3d_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
