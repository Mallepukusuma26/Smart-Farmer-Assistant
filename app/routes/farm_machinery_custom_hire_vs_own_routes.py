"""
FarmMachineryCustomHireVsOwnEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.farm_machinery_custom_hire_vs_own_controller import FarmMachineryCustomHireVsOwnEngineController

farm_machinery_custom_hire_vs_own_bp = Blueprint("farm-machinery-custom-hire-vs-own", __name__, url_prefix="/api/farm-machinery-custom-hire-vs-own")
controller = FarmMachineryCustomHireVsOwnEngineController()

@farm_machinery_custom_hire_vs_own_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@farm_machinery_custom_hire_vs_own_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@farm_machinery_custom_hire_vs_own_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
