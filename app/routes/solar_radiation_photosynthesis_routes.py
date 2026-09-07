"""
Photosynthetic Radiation & Canopy Light Extinction Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.solar_radiation_photosynthesis_controller import CanopyPhotosynthesisEngineController

solar_radiation_photosynthesis_engine_bp = Blueprint("solar-radiation-photosynthesis", __name__, url_prefix="/api/solar-radiation-photosynthesis")
controller = CanopyPhotosynthesisEngineController()

@solar_radiation_photosynthesis_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@solar_radiation_photosynthesis_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
