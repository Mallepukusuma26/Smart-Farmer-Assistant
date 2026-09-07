"""
FertigationDripInjectionRateEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.fertigation_drip_injection_rate_lph_controller import FertigationDripInjectionRateEngineController

fertigation_drip_injection_rate_lph_bp = Blueprint("fertigation-drip-injection-rate-lph", __name__, url_prefix="/api/fertigation-drip-injection-rate-lph")
controller = FertigationDripInjectionRateEngineController()

@fertigation_drip_injection_rate_lph_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@fertigation_drip_injection_rate_lph_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@fertigation_drip_injection_rate_lph_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
