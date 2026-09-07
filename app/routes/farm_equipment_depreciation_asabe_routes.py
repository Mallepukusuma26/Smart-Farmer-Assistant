"""
ASABE Equipment Depreciation & Repair Cost Engine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.farm_equipment_depreciation_asabe_controller import ASABEEquipmentDepreciationEngineController

farm_equipment_depreciation_asabe_engine_bp = Blueprint("farm-equipment-depreciation-asabe", __name__, url_prefix="/api/farm-equipment-depreciation-asabe")
controller = ASABEEquipmentDepreciationEngineController()

@farm_equipment_depreciation_asabe_engine_bp.route("/calculate", methods=["POST"])
def calculate():
    return controller.calculate()

@farm_equipment_depreciation_asabe_engine_bp.route("/evaluate-scenario", methods=["POST"])
def evaluate_scenario():
    return controller.evaluate_scenario()
