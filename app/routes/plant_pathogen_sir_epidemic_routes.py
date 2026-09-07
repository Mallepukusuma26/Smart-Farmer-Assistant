"""
Plant Disease SIR Epidemic Progression Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.plant_pathogen_sir_epidemic_controller import PathogenSIREpidemicEngineController

plant_pathogen_sir_epidemic_engine_bp = Blueprint("plant-pathogen-sir-epidemic", __name__, url_prefix="/api/plant-pathogen-sir-epidemic")
controller = PathogenSIREpidemicEngineController()

@plant_pathogen_sir_epidemic_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@plant_pathogen_sir_epidemic_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
