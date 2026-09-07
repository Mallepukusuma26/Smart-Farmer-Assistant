"""
AgronomyPrecisionFertigationDosingEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_precision_fertigation_dosing_controller import AgronomyPrecisionFertigationDosingEngineController

agronomy_precision_fertigation_dosing_bp = Blueprint("agronomy-precision-fertigation-dosing", __name__, url_prefix="/api/agronomy-precision-fertigation-dosing")
ctrl = AgronomyPrecisionFertigationDosingEngineController()

@agronomy_precision_fertigation_dosing_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
