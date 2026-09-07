"""
FoodSafetyHACCPHazardMatrixEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.food_safety_haccp_hazard_matrix_controller import FoodSafetyHACCPHazardMatrixEngineController

food_safety_haccp_hazard_matrix_bp = Blueprint("food-safety-haccp-hazard-matrix", __name__, url_prefix="/api/food-safety-haccp-hazard-matrix")
controller = FoodSafetyHACCPHazardMatrixEngineController()

@food_safety_haccp_hazard_matrix_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@food_safety_haccp_hazard_matrix_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@food_safety_haccp_hazard_matrix_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
