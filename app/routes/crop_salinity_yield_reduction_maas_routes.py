"""
CropSalinityYieldReductionMaasEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_salinity_yield_reduction_maas_controller import CropSalinityYieldReductionMaasEngineController

crop_salinity_yield_reduction_maas_bp = Blueprint("crop-salinity-yield-reduction-maas", __name__, url_prefix="/api/crop-salinity-yield-reduction-maas")
controller = CropSalinityYieldReductionMaasEngineController()

@crop_salinity_yield_reduction_maas_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_salinity_yield_reduction_maas_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_salinity_yield_reduction_maas_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
