"""
OrganicBiocharAmendmentStabilityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.organic_biochar_amendment_stability_controller import OrganicBiocharAmendmentStabilityEngineController

organic_biochar_amendment_stability_bp = Blueprint("organic-biochar-amendment-stability", __name__, url_prefix="/api/organic-biochar-amendment-stability")
controller = OrganicBiocharAmendmentStabilityEngineController()

@organic_biochar_amendment_stability_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@organic_biochar_amendment_stability_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@organic_biochar_amendment_stability_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
