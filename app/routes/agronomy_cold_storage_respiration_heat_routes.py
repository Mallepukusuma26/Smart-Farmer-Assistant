"""
AgronomyColdStorageRespirationHeatEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_cold_storage_respiration_heat_controller import AgronomyColdStorageRespirationHeatEngineController

agronomy_cold_storage_respiration_heat_bp = Blueprint("agronomy-cold-storage-respiration-heat", __name__, url_prefix="/api/agronomy-cold-storage-respiration-heat")
controller = AgronomyColdStorageRespirationHeatEngineController()

@agronomy_cold_storage_respiration_heat_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_cold_storage_respiration_heat_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
