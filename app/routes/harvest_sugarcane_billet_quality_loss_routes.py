"""
HarvestSugarcaneBilletQualityLossEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.harvest_sugarcane_billet_quality_loss_controller import HarvestSugarcaneBilletQualityLossEngineController

harvest_sugarcane_billet_quality_loss_bp = Blueprint("harvest-sugarcane-billet-quality-loss", __name__, url_prefix="/api/harvest-sugarcane-billet-quality-loss")
controller = HarvestSugarcaneBilletQualityLossEngineController()

@harvest_sugarcane_billet_quality_loss_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@harvest_sugarcane_billet_quality_loss_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@harvest_sugarcane_billet_quality_loss_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
