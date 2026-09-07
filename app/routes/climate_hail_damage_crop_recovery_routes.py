"""
ClimateHailDamageCropRecoveryEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.climate_hail_damage_crop_recovery_controller import ClimateHailDamageCropRecoveryEngineController

climate_hail_damage_crop_recovery_bp = Blueprint("climate-hail-damage-crop-recovery", __name__, url_prefix="/api/climate-hail-damage-crop-recovery")
controller = ClimateHailDamageCropRecoveryEngineController()

@climate_hail_damage_crop_recovery_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@climate_hail_damage_crop_recovery_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@climate_hail_damage_crop_recovery_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
