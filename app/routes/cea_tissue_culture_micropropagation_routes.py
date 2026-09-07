"""
CEATissueCultureMicropropagationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.cea_tissue_culture_micropropagation_controller import CEATissueCultureMicropropagationEngineController

cea_tissue_culture_micropropagation_bp = Blueprint("cea-tissue-culture-micropropagation", __name__, url_prefix="/api/cea-tissue-culture-micropropagation")
controller = CEATissueCultureMicropropagationEngineController()

@cea_tissue_culture_micropropagation_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@cea_tissue_culture_micropropagation_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@cea_tissue_culture_micropropagation_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
