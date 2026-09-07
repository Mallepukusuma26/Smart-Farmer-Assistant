"""
EnergyBiomassPelletCalorificValueEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.energy_biomass_pellet_calorific_value_controller import EnergyBiomassPelletCalorificValueEngineController

energy_biomass_pellet_calorific_value_bp = Blueprint("energy-biomass-pellet-calorific-value", __name__, url_prefix="/api/energy-biomass-pellet-calorific-value")
controller = EnergyBiomassPelletCalorificValueEngineController()

@energy_biomass_pellet_calorific_value_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@energy_biomass_pellet_calorific_value_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@energy_biomass_pellet_calorific_value_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
