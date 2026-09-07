"""
RGB Spectral Vigor & Simulated NDVI Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_canopy_reflectance_ndvi_controller import SpectralNDVIEngineController

crop_canopy_reflectance_ndvi_engine_bp = Blueprint("crop-canopy-reflectance-ndvi", __name__, url_prefix="/api/crop-canopy-reflectance-ndvi")
controller = SpectralNDVIEngineController()

@crop_canopy_reflectance_ndvi_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@crop_canopy_reflectance_ndvi_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
