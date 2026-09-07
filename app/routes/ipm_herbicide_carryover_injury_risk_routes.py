"""
IPMHerbicideCarryoverInjuryRiskEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.ipm_herbicide_carryover_injury_risk_controller import IPMHerbicideCarryoverInjuryRiskEngineController

ipm_herbicide_carryover_injury_risk_bp = Blueprint("ipm-herbicide-carryover-injury-risk", __name__, url_prefix="/api/ipm-herbicide-carryover-injury-risk")
controller = IPMHerbicideCarryoverInjuryRiskEngineController()

@ipm_herbicide_carryover_injury_risk_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@ipm_herbicide_carryover_injury_risk_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@ipm_herbicide_carryover_injury_risk_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
