"""
AgronomyPestDegreeDayPhenologyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_pest_degree_day_phenology_controller import AgronomyPestDegreeDayPhenologyEngineController

agronomy_pest_degree_day_phenology_bp = Blueprint("agronomy-pest-degree-day-phenology", __name__, url_prefix="/api/agronomy-pest-degree-day-phenology")
controller = AgronomyPestDegreeDayPhenologyEngineController()

@agronomy_pest_degree_day_phenology_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_pest_degree_day_phenology_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
