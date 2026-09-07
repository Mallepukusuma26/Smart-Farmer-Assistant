"""
AgronomySoilOrganicMatterLabileCEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_soil_organic_matter_labile_c_controller import AgronomySoilOrganicMatterLabileCEngineController

agronomy_soil_organic_matter_labile_c_bp = Blueprint("agronomy-soil-organic-matter-labile-c", __name__, url_prefix="/api/agronomy-soil-organic-matter-labile-c")
ctrl = AgronomySoilOrganicMatterLabileCEngineController()

@agronomy_soil_organic_matter_labile_c_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
