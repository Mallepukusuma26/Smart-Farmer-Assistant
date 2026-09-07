"""
CarbonCreditOffsetQuantifierEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.carbon_credit_offset_quantifier_controller import CarbonCreditOffsetQuantifierEngineController

carbon_credit_offset_quantifier_bp = Blueprint("carbon-credit-offset-quantifier", __name__, url_prefix="/api/carbon-credit-offset-quantifier")
controller = CarbonCreditOffsetQuantifierEngineController()

@carbon_credit_offset_quantifier_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@carbon_credit_offset_quantifier_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@carbon_credit_offset_quantifier_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
