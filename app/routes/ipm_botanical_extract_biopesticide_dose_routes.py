"""
IPMBotanicalExtractBiopesticideDoseEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.ipm_botanical_extract_biopesticide_dose_controller import IPMBotanicalExtractBiopesticideDoseEngineController

ipm_botanical_extract_biopesticide_dose_bp = Blueprint("ipm-botanical-extract-biopesticide-dose", __name__, url_prefix="/api/ipm-botanical-extract-biopesticide-dose")
controller = IPMBotanicalExtractBiopesticideDoseEngineController()

@ipm_botanical_extract_biopesticide_dose_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@ipm_botanical_extract_biopesticide_dose_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@ipm_botanical_extract_biopesticide_dose_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
