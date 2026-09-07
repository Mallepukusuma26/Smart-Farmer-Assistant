"""
AgronomyAquaponicsTANNitrificationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_aquaponics_tan_nitrification_controller import AgronomyAquaponicsTANNitrificationEngineController

agronomy_aquaponics_tan_nitrification_bp = Blueprint("agronomy-aquaponics-tan-nitrification", __name__, url_prefix="/api/agronomy-aquaponics-tan-nitrification")
controller = AgronomyAquaponicsTANNitrificationEngineController()

@agronomy_aquaponics_tan_nitrification_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_aquaponics_tan_nitrification_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
