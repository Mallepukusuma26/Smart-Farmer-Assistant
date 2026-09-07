"""
CropSpectralNDVIVigorProxyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_spectral_ndvi_vigor_proxy_controller import CropSpectralNDVIVigorProxyEngineController

crop_spectral_ndvi_vigor_proxy_bp = Blueprint("crop-spectral-ndvi-vigor-proxy", __name__, url_prefix="/api/crop-spectral-ndvi-vigor-proxy")
controller = CropSpectralNDVIVigorProxyEngineController()

@crop_spectral_ndvi_vigor_proxy_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_spectral_ndvi_vigor_proxy_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_spectral_ndvi_vigor_proxy_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
