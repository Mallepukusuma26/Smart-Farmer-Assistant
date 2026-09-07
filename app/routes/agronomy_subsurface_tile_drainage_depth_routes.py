"""
AgronomySubsurfaceTileDrainageDepthEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_subsurface_tile_drainage_depth_controller import AgronomySubsurfaceTileDrainageDepthEngineController

agronomy_subsurface_tile_drainage_depth_bp = Blueprint("agronomy-subsurface-tile-drainage-depth", __name__, url_prefix="/api/agronomy-subsurface-tile-drainage-depth")
ctrl = AgronomySubsurfaceTileDrainageDepthEngineController()

@agronomy_subsurface_tile_drainage_depth_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
