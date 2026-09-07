"""
AgronomySoilOrganicMatterHumificationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_soil_organic_matter_humification_controller import AgronomySoilOrganicMatterHumificationEngineController

agronomy_soil_organic_matter_humification_bp = Blueprint("agronomy-soil-organic-matter-humification", __name__, url_prefix="/api/agronomy-soil-organic-matter-humification")
controller = AgronomySoilOrganicMatterHumificationEngineController()

@agronomy_soil_organic_matter_humification_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_soil_organic_matter_humification_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
