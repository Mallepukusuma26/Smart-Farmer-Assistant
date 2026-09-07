"""
ContractFarmingOutgrowerPayoutEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.contract_farming_outgrower_payout_controller import ContractFarmingOutgrowerPayoutEngineController

contract_farming_outgrower_payout_bp = Blueprint("contract-farming-outgrower-payout", __name__, url_prefix="/api/contract-farming-outgrower-payout")
controller = ContractFarmingOutgrowerPayoutEngineController()

@contract_farming_outgrower_payout_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@contract_farming_outgrower_payout_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@contract_farming_outgrower_payout_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
