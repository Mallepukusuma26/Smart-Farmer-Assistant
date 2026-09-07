"""
FertigationFoliarSprayAbsorptionEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertigation_foliar_spray_absorption_controller import FertigationFoliarSprayAbsorptionEngineController

fertigation_foliar_spray_absorption_bp = Blueprint("fertigation-foliar-spray-absorption", __name__, url_prefix="/api/fertigation-foliar-spray-absorption")
controller = FertigationFoliarSprayAbsorptionEngineController()

@fertigation_foliar_spray_absorption_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@fertigation_foliar_spray_absorption_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@fertigation_foliar_spray_absorption_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
