"""
ProcessingCoffeeFermentationWashingEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.processing_coffee_fermentation_washing_controller import ProcessingCoffeeFermentationWashingEngineController

processing_coffee_fermentation_washing_bp = Blueprint("processing-coffee-fermentation-washing", __name__, url_prefix="/api/processing-coffee-fermentation-washing")
controller = ProcessingCoffeeFermentationWashingEngineController()

@processing_coffee_fermentation_washing_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@processing_coffee_fermentation_washing_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@processing_coffee_fermentation_washing_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
