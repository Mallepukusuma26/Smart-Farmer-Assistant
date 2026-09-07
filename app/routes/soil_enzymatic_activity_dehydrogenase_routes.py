"""
SoilEnzymaticActivityDehydrogenaseEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_enzymatic_activity_dehydrogenase_controller import SoilEnzymaticActivityDehydrogenaseEngineController

soil_enzymatic_activity_dehydrogenase_bp = Blueprint("soil-enzymatic-activity-dehydrogenase", __name__, url_prefix="/api/soil-enzymatic-activity-dehydrogenase")
controller = SoilEnzymaticActivityDehydrogenaseEngineController()

@soil_enzymatic_activity_dehydrogenase_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@soil_enzymatic_activity_dehydrogenase_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@soil_enzymatic_activity_dehydrogenase_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
