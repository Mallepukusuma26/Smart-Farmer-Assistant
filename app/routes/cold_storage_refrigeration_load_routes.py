"""
ColdStorageRefrigerationLoadEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.cold_storage_refrigeration_load_controller import ColdStorageRefrigerationLoadEngineController

cold_storage_refrigeration_load_bp = Blueprint("cold-storage-refrigeration-load", __name__, url_prefix="/api/cold-storage-refrigeration-load")
controller = ColdStorageRefrigerationLoadEngineController()

@cold_storage_refrigeration_load_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@cold_storage_refrigeration_load_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@cold_storage_refrigeration_load_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
