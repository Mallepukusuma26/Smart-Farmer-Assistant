"""
IrrigationSubsurfaceDripSDIDepthEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.irrigation_subsurface_drip_sdi_depth_controller import IrrigationSubsurfaceDripSDIDepthEngineController

irrigation_subsurface_drip_sdi_depth_bp = Blueprint("irrigation-subsurface-drip-sdi-depth", __name__, url_prefix="/api/irrigation-subsurface-drip-sdi-depth")
controller = IrrigationSubsurfaceDripSDIDepthEngineController()

@irrigation_subsurface_drip_sdi_depth_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@irrigation_subsurface_drip_sdi_depth_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@irrigation_subsurface_drip_sdi_depth_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
