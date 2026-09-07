"""
GrainStorageHedgingMarginEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.grain_storage_hedging_margin_controller import GrainStorageHedgingMarginEngineController

grain_storage_hedging_margin_bp = Blueprint("grain-storage-hedging-margin", __name__, url_prefix="/api/grain-storage-hedging-margin")
controller = GrainStorageHedgingMarginEngineController()

@grain_storage_hedging_margin_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@grain_storage_hedging_margin_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@grain_storage_hedging_margin_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
