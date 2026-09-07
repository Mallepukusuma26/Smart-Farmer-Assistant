"""
FertigationCalciumNitrateCompatibilityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertigation_calcium_nitrate_compatibility_controller import FertigationCalciumNitrateCompatibilityEngineController

fertigation_calcium_nitrate_compatibility_bp = Blueprint("fertigation-calcium-nitrate-compatibility", __name__, url_prefix="/api/fertigation-calcium-nitrate-compatibility")
controller = FertigationCalciumNitrateCompatibilityEngineController()

@fertigation_calcium_nitrate_compatibility_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@fertigation_calcium_nitrate_compatibility_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@fertigation_calcium_nitrate_compatibility_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
