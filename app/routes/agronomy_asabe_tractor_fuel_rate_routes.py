"""
AgronomyASABETractorFuelRateEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_asabe_tractor_fuel_rate_controller import AgronomyASABETractorFuelRateEngineController

agronomy_asabe_tractor_fuel_rate_bp = Blueprint("agronomy-asabe-tractor-fuel-rate", __name__, url_prefix="/api/agronomy-asabe-tractor-fuel-rate")
controller = AgronomyASABETractorFuelRateEngineController()

@agronomy_asabe_tractor_fuel_rate_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_asabe_tractor_fuel_rate_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
