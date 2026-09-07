"""
AgronomyCropCanopyReflectanceProxyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_crop_canopy_reflectance_proxy_controller import AgronomyCropCanopyReflectanceProxyEngineController

agronomy_crop_canopy_reflectance_proxy_bp = Blueprint("agronomy-crop-canopy-reflectance-proxy", __name__, url_prefix="/api/agronomy-crop-canopy-reflectance-proxy")
controller = AgronomyCropCanopyReflectanceProxyEngineController()

@agronomy_crop_canopy_reflectance_proxy_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_crop_canopy_reflectance_proxy_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
