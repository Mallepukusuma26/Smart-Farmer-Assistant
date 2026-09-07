"""
Greenhouse Vapor Pressure Deficit & Heating Load Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.greenhouse_microclimate_vpd_controller import GreenhouseVPDEngineController

greenhouse_microclimate_vpd_engine_bp = Blueprint("greenhouse-microclimate-vpd", __name__, url_prefix="/api/greenhouse-microclimate-vpd")
controller = GreenhouseVPDEngineController()

@greenhouse_microclimate_vpd_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@greenhouse_microclimate_vpd_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
