"""
OrganicVermicompostNutrientEnrichmentEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.organic_vermicompost_nutrient_enrichment_controller import OrganicVermicompostNutrientEnrichmentEngineController

organic_vermicompost_nutrient_enrichment_bp = Blueprint("organic-vermicompost-nutrient-enrichment", __name__, url_prefix="/api/organic-vermicompost-nutrient-enrichment")
controller = OrganicVermicompostNutrientEnrichmentEngineController()

@organic_vermicompost_nutrient_enrichment_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@organic_vermicompost_nutrient_enrichment_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@organic_vermicompost_nutrient_enrichment_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
