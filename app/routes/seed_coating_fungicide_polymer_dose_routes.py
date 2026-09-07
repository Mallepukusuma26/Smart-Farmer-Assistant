"""
SeedCoatingFungicidePolymerDoseEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.seed_coating_fungicide_polymer_dose_controller import SeedCoatingFungicidePolymerDoseEngineController

seed_coating_fungicide_polymer_dose_bp = Blueprint("seed-coating-fungicide-polymer-dose", __name__, url_prefix="/api/seed-coating-fungicide-polymer-dose")
controller = SeedCoatingFungicidePolymerDoseEngineController()

@seed_coating_fungicide_polymer_dose_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@seed_coating_fungicide_polymer_dose_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@seed_coating_fungicide_polymer_dose_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
