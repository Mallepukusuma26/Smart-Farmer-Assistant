"""
HarvestGrainMoistureCombineLossesEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.harvest_grain_moisture_combine_losses_controller import HarvestGrainMoistureCombineLossesEngineController

harvest_grain_moisture_combine_losses_bp = Blueprint("harvest-grain-moisture-combine-losses", __name__, url_prefix="/api/harvest-grain-moisture-combine-losses")
controller = HarvestGrainMoistureCombineLossesEngineController()

@harvest_grain_moisture_combine_losses_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@harvest_grain_moisture_combine_losses_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@harvest_grain_moisture_combine_losses_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
