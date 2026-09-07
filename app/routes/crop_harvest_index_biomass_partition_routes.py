"""
CropHarvestIndexBiomassPartitionEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.crop_harvest_index_biomass_partition_controller import CropHarvestIndexBiomassPartitionEngineController

crop_harvest_index_biomass_partition_bp = Blueprint("crop-harvest-index-biomass-partition", __name__, url_prefix="/api/crop-harvest-index-biomass-partition")
controller = CropHarvestIndexBiomassPartitionEngineController()

@crop_harvest_index_biomass_partition_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@crop_harvest_index_biomass_partition_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@crop_harvest_index_biomass_partition_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
