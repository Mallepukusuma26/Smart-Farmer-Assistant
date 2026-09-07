"""
CEAVerticalFarmLEDSpectrumPAREngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.cea_vertical_farm_led_spectrum_par_controller import CEAVerticalFarmLEDSpectrumPAREngineController

cea_vertical_farm_led_spectrum_par_bp = Blueprint("cea-vertical-farm-led-spectrum-par", __name__, url_prefix="/api/cea-vertical-farm-led-spectrum-par")
controller = CEAVerticalFarmLEDSpectrumPAREngineController()

@cea_vertical_farm_led_spectrum_par_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@cea_vertical_farm_led_spectrum_par_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@cea_vertical_farm_led_spectrum_par_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
