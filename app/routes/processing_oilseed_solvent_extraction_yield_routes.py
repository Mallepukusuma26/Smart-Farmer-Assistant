"""
ProcessingOilseedSolventExtractionYieldEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.processing_oilseed_solvent_extraction_yield_controller import ProcessingOilseedSolventExtractionYieldEngineController

processing_oilseed_solvent_extraction_yield_bp = Blueprint("processing-oilseed-solvent-extraction-yield", __name__, url_prefix="/api/processing-oilseed-solvent-extraction-yield")
controller = ProcessingOilseedSolventExtractionYieldEngineController()

@processing_oilseed_solvent_extraction_yield_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@processing_oilseed_solvent_extraction_yield_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@processing_oilseed_solvent_extraction_yield_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
