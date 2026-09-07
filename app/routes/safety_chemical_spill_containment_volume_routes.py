"""
SafetyChemicalSpillContainmentVolumeEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.safety_chemical_spill_containment_volume_controller import SafetyChemicalSpillContainmentVolumeEngineController

safety_chemical_spill_containment_volume_bp = Blueprint("safety-chemical-spill-containment-volume", __name__, url_prefix="/api/safety-chemical-spill-containment-volume")
controller = SafetyChemicalSpillContainmentVolumeEngineController()

@safety_chemical_spill_containment_volume_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@safety_chemical_spill_containment_volume_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@safety_chemical_spill_containment_volume_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
