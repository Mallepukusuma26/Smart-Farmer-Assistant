"""
FertigationMicronutrientChelateStabilityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertigation_micronutrient_chelate_stability_controller import FertigationMicronutrientChelateStabilityEngineController

fertigation_micronutrient_chelate_stability_bp = Blueprint("fertigation-micronutrient-chelate-stability", __name__, url_prefix="/api/fertigation-micronutrient-chelate-stability")
controller = FertigationMicronutrientChelateStabilityEngineController()

@fertigation_micronutrient_chelate_stability_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@fertigation_micronutrient_chelate_stability_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@fertigation_micronutrient_chelate_stability_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
