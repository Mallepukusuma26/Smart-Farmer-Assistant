"""
HarvestCottonPickerSpindleEfficiencyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.harvest_cotton_picker_spindle_efficiency_controller import HarvestCottonPickerSpindleEfficiencyEngineController

harvest_cotton_picker_spindle_efficiency_bp = Blueprint("harvest-cotton-picker-spindle-efficiency", __name__, url_prefix="/api/harvest-cotton-picker-spindle-efficiency")
controller = HarvestCottonPickerSpindleEfficiencyEngineController()

@harvest_cotton_picker_spindle_efficiency_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@harvest_cotton_picker_spindle_efficiency_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@harvest_cotton_picker_spindle_efficiency_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
