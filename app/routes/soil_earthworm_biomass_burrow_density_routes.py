"""
SoilEarthwormBiomassBurrowEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_earthworm_biomass_burrow_density_controller import SoilEarthwormBiomassBurrowEngineController

soil_earthworm_biomass_burrow_density_bp = Blueprint("soil-earthworm-biomass-burrow-density", __name__, url_prefix="/api/soil-earthworm-biomass-burrow-density")
controller = SoilEarthwormBiomassBurrowEngineController()

@soil_earthworm_biomass_burrow_density_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@soil_earthworm_biomass_burrow_density_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@soil_earthworm_biomass_burrow_density_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
