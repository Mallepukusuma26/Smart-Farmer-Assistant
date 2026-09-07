"""
ProcessingRiceMillingOutturnRatioEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.processing_rice_milling_outturn_ratio_controller import ProcessingRiceMillingOutturnRatioEngineController

processing_rice_milling_outturn_ratio_bp = Blueprint("processing-rice-milling-outturn-ratio", __name__, url_prefix="/api/processing-rice-milling-outturn-ratio")
controller = ProcessingRiceMillingOutturnRatioEngineController()

@processing_rice_milling_outturn_ratio_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@processing_rice_milling_outturn_ratio_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@processing_rice_milling_outturn_ratio_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
