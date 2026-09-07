"""
AgronomyEquipmentDepreciationSalvageEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_equipment_depreciation_salvage_controller import AgronomyEquipmentDepreciationSalvageEngineController

agronomy_equipment_depreciation_salvage_bp = Blueprint("agronomy-equipment-depreciation-salvage", __name__, url_prefix="/api/agronomy-equipment-depreciation-salvage")
controller = AgronomyEquipmentDepreciationSalvageEngineController()

@agronomy_equipment_depreciation_salvage_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_equipment_depreciation_salvage_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
