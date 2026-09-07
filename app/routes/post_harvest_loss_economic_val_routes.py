"""
PostHarvestLossEconomicValEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.post_harvest_loss_economic_val_controller import PostHarvestLossEconomicValEngineController

post_harvest_loss_economic_val_bp = Blueprint("post-harvest-loss-economic-val", __name__, url_prefix="/api/post-harvest-loss-economic-val")
controller = PostHarvestLossEconomicValEngineController()

@post_harvest_loss_economic_val_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@post_harvest_loss_economic_val_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@post_harvest_loss_economic_val_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
