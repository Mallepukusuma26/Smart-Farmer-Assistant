"""
SeedCoatDormancyScarificationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.seed_coat_dormancy_scarification_controller import SeedCoatDormancyScarificationEngineController

seed_coat_dormancy_scarification_bp = Blueprint("seed-coat-dormancy-scarification", __name__, url_prefix="/api/seed-coat-dormancy-scarification")
controller = SeedCoatDormancyScarificationEngineController()

@seed_coat_dormancy_scarification_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@seed_coat_dormancy_scarification_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@seed_coat_dormancy_scarification_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
