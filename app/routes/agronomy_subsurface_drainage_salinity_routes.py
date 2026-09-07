"""
AgronomySubsurfaceDrainageSalinityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_subsurface_drainage_salinity_controller import AgronomySubsurfaceDrainageSalinityEngineController

agronomy_subsurface_drainage_salinity_bp = Blueprint("agronomy-subsurface-drainage-salinity", __name__, url_prefix="/api/agronomy-subsurface-drainage-salinity")
controller = AgronomySubsurfaceDrainageSalinityEngineController()

@agronomy_subsurface_drainage_salinity_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_subsurface_drainage_salinity_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
