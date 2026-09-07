"""
LivestockMethaneEntericFermentationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.livestock_methane_enteric_fermentation_controller import LivestockMethaneEntericFermentationEngineController

livestock_methane_enteric_fermentation_bp = Blueprint("livestock-methane-enteric-fermentation", __name__, url_prefix="/api/livestock-methane-enteric-fermentation")
controller = LivestockMethaneEntericFermentationEngineController()

@livestock_methane_enteric_fermentation_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@livestock_methane_enteric_fermentation_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@livestock_methane_enteric_fermentation_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
