"""
OrganicBiodynamicPreparationCalendarEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.organic_biodynamic_preparation_calendar_controller import OrganicBiodynamicPreparationCalendarEngineController

organic_biodynamic_preparation_calendar_bp = Blueprint("organic-biodynamic-preparation-calendar", __name__, url_prefix="/api/organic-biodynamic-preparation-calendar")
controller = OrganicBiodynamicPreparationCalendarEngineController()

@organic_biodynamic_preparation_calendar_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@organic_biodynamic_preparation_calendar_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@organic_biodynamic_preparation_calendar_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
