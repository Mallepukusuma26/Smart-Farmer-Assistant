"""
OrganicPushPullPestManagementEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.organic_push_pull_pest_management_controller import OrganicPushPullPestManagementEngineController

organic_push_pull_pest_management_bp = Blueprint("organic-push-pull-pest-management", __name__, url_prefix="/api/organic-push-pull-pest-management")
controller = OrganicPushPullPestManagementEngineController()

@organic_push_pull_pest_management_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@organic_push_pull_pest_management_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@organic_push_pull_pest_management_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
