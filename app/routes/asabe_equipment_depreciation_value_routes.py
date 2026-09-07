"""
ASABEEquipmentDepreciationValueEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.asabe_equipment_depreciation_value_controller import ASABEEquipmentDepreciationValueEngineController

asabe_equipment_depreciation_value_bp = Blueprint("asabe-equipment-depreciation-value", __name__, url_prefix="/api/asabe-equipment-depreciation-value")
controller = ASABEEquipmentDepreciationValueEngineController()

@asabe_equipment_depreciation_value_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@asabe_equipment_depreciation_value_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@asabe_equipment_depreciation_value_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
