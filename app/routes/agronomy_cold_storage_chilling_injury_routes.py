"""
AgronomyColdStorageChillingInjuryEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_cold_storage_chilling_injury_controller import AgronomyColdStorageChillingInjuryEngineController

agronomy_cold_storage_chilling_injury_bp = Blueprint("agronomy-cold-storage-chilling-injury", __name__, url_prefix="/api/agronomy-cold-storage-chilling-injury")
ctrl = AgronomyColdStorageChillingInjuryEngineController()

@agronomy_cold_storage_chilling_injury_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
