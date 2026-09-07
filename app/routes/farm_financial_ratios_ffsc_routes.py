"""
FarmFinancialRatiosFSCSEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.farm_financial_ratios_ffsc_controller import FarmFinancialRatiosFSCSEngineController

farm_financial_ratios_ffsc_bp = Blueprint("farm-financial-ratios-ffsc", __name__, url_prefix="/api/farm-financial-ratios-ffsc")
controller = FarmFinancialRatiosFSCSEngineController()

@farm_financial_ratios_ffsc_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@farm_financial_ratios_ffsc_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@farm_financial_ratios_ffsc_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
