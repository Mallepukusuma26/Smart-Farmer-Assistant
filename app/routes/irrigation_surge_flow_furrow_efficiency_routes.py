"""
IrrigationSurgeFlowFurrowEfficiencyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.irrigation_surge_flow_furrow_efficiency_controller import IrrigationSurgeFlowFurrowEfficiencyEngineController

irrigation_surge_flow_furrow_efficiency_bp = Blueprint("irrigation-surge-flow-furrow-efficiency", __name__, url_prefix="/api/irrigation-surge-flow-furrow-efficiency")
controller = IrrigationSurgeFlowFurrowEfficiencyEngineController()

@irrigation_surge_flow_furrow_efficiency_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@irrigation_surge_flow_furrow_efficiency_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@irrigation_surge_flow_furrow_efficiency_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
