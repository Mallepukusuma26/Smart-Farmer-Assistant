"""
CEAHydroponicNutrientSolutionPPMEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.cea_hydroponic_nutrient_solution_ppm_controller import CEAHydroponicNutrientSolutionPPMEngineController

cea_hydroponic_nutrient_solution_ppm_bp = Blueprint("cea-hydroponic-nutrient-solution-ppm", __name__, url_prefix="/api/cea-hydroponic-nutrient-solution-ppm")
controller = CEAHydroponicNutrientSolutionPPMEngineController()

@cea_hydroponic_nutrient_solution_ppm_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@cea_hydroponic_nutrient_solution_ppm_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@cea_hydroponic_nutrient_solution_ppm_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
