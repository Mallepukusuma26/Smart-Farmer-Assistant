"""
SeedHybridPurityElectrophoresisEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.seed_hybrid_purity_electrophoresis_controller import SeedHybridPurityElectrophoresisEngineController

seed_hybrid_purity_electrophoresis_bp = Blueprint("seed-hybrid-purity-electrophoresis", __name__, url_prefix="/api/seed-hybrid-purity-electrophoresis")
controller = SeedHybridPurityElectrophoresisEngineController()

@seed_hybrid_purity_electrophoresis_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@seed_hybrid_purity_electrophoresis_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@seed_hybrid_purity_electrophoresis_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
