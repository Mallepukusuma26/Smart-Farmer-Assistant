"""
OrganicCoverCropNitrogenReleaseEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.organic_cover_crop_nitrogen_release_controller import OrganicCoverCropNitrogenReleaseEngineController

organic_cover_crop_nitrogen_release_bp = Blueprint("organic-cover-crop-nitrogen-release", __name__, url_prefix="/api/organic-cover-crop-nitrogen-release")
controller = OrganicCoverCropNitrogenReleaseEngineController()

@organic_cover_crop_nitrogen_release_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@organic_cover_crop_nitrogen_release_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@organic_cover_crop_nitrogen_release_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
