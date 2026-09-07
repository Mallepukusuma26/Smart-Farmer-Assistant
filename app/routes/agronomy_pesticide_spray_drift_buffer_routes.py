"""
AgronomyPesticideSprayDriftBufferEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_pesticide_spray_drift_buffer_controller import AgronomyPesticideSprayDriftBufferEngineController

agronomy_pesticide_spray_drift_buffer_bp = Blueprint("agronomy-pesticide-spray-drift-buffer", __name__, url_prefix="/api/agronomy-pesticide-spray-drift-buffer")
ctrl = AgronomyPesticideSprayDriftBufferEngineController()

@agronomy_pesticide_spray_drift_buffer_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
