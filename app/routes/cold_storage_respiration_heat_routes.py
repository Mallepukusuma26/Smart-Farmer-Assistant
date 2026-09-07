"""
Cold Storage Fruit Respiration & Heat Load Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.cold_storage_respiration_heat_controller import ColdStorageRespirationEngineController

cold_storage_respiration_heat_engine_bp = Blueprint("cold-storage-respiration-heat", __name__, url_prefix="/api/cold-storage-respiration-heat")
controller = ColdStorageRespirationEngineController()

@cold_storage_respiration_heat_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@cold_storage_respiration_heat_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
