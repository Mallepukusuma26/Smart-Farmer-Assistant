"""
SoilNematodeCommunityStructureEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_nematode_community_structure_controller import SoilNematodeCommunityStructureEngineController

soil_nematode_community_structure_bp = Blueprint("soil-nematode-community-structure", __name__, url_prefix="/api/soil-nematode-community-structure")
controller = SoilNematodeCommunityStructureEngineController()

@soil_nematode_community_structure_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@soil_nematode_community_structure_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@soil_nematode_community_structure_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
