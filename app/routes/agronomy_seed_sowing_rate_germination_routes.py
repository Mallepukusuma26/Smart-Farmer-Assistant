"""
AgronomySeedSowingRateGerminationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_seed_sowing_rate_germination_controller import AgronomySeedSowingRateGerminationEngineController

agronomy_seed_sowing_rate_germination_bp = Blueprint("agronomy-seed-sowing-rate-germination", __name__, url_prefix="/api/agronomy-seed-sowing-rate-germination")
controller = AgronomySeedSowingRateGerminationEngineController()

@agronomy_seed_sowing_rate_germination_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_seed_sowing_rate_germination_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
