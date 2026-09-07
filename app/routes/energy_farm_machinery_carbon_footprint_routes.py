"""
EnergyFarmMachineryCarbonFootprintEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.energy_farm_machinery_carbon_footprint_controller import EnergyFarmMachineryCarbonFootprintEngineController

energy_farm_machinery_carbon_footprint_bp = Blueprint("energy-farm-machinery-carbon-footprint", __name__, url_prefix="/api/energy-farm-machinery-carbon-footprint")
controller = EnergyFarmMachineryCarbonFootprintEngineController()

@energy_farm_machinery_carbon_footprint_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@energy_farm_machinery_carbon_footprint_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@energy_farm_machinery_carbon_footprint_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
