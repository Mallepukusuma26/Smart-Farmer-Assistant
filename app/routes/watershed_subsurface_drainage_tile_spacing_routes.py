"""
WatershedSubsurfaceDrainageTileEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.watershed_subsurface_drainage_tile_spacing_controller import WatershedSubsurfaceDrainageTileEngineController

watershed_subsurface_drainage_tile_spacing_bp = Blueprint("watershed-subsurface-drainage-tile-spacing", __name__, url_prefix="/api/watershed-subsurface-drainage-tile-spacing")
controller = WatershedSubsurfaceDrainageTileEngineController()

@watershed_subsurface_drainage_tile_spacing_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@watershed_subsurface_drainage_tile_spacing_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@watershed_subsurface_drainage_tile_spacing_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
