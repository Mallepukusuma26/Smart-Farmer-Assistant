"""
SoilMycorrhizalFungalColonizationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_mycorrhizal_fungal_colonization_controller import SoilMycorrhizalFungalColonizationEngineController

soil_mycorrhizal_fungal_colonization_bp = Blueprint("soil-mycorrhizal-fungal-colonization", __name__, url_prefix="/api/soil-mycorrhizal-fungal-colonization")
controller = SoilMycorrhizalFungalColonizationEngineController()

@soil_mycorrhizal_fungal_colonization_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@soil_mycorrhizal_fungal_colonization_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@soil_mycorrhizal_fungal_colonization_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
