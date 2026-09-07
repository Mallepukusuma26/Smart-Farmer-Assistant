"""
LivestockManureNutrientExcretionIPCCEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.livestock_manure_nutrient_excretion_ipcc_controller import LivestockManureNutrientExcretionIPCCEngineController

livestock_manure_nutrient_excretion_ipcc_bp = Blueprint("livestock-manure-nutrient-excretion-ipcc", __name__, url_prefix="/api/livestock-manure-nutrient-excretion-ipcc")
controller = LivestockManureNutrientExcretionIPCCEngineController()

@livestock_manure_nutrient_excretion_ipcc_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@livestock_manure_nutrient_excretion_ipcc_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@livestock_manure_nutrient_excretion_ipcc_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
