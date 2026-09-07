"""
SeedVigorAcceleratedAgingTestEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.seed_vigor_accelerated_aging_test_controller import SeedVigorAcceleratedAgingTestEngineController

seed_vigor_accelerated_aging_test_bp = Blueprint("seed-vigor-accelerated-aging-test", __name__, url_prefix="/api/seed-vigor-accelerated-aging-test")
controller = SeedVigorAcceleratedAgingTestEngineController()

@seed_vigor_accelerated_aging_test_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@seed_vigor_accelerated_aging_test_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@seed_vigor_accelerated_aging_test_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
