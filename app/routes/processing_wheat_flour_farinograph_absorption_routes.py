"""
ProcessingWheatFlourFarinographAbsorptionEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.processing_wheat_flour_farinograph_absorption_controller import ProcessingWheatFlourFarinographAbsorptionEngineController

processing_wheat_flour_farinograph_absorption_bp = Blueprint("processing-wheat-flour-farinograph-absorption", __name__, url_prefix="/api/processing-wheat-flour-farinograph-absorption")
controller = ProcessingWheatFlourFarinographAbsorptionEngineController()

@processing_wheat_flour_farinograph_absorption_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@processing_wheat_flour_farinograph_absorption_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@processing_wheat_flour_farinograph_absorption_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
