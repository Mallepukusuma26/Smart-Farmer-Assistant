"""
AgronomyAquacultureWaterRecirculationEngine Routes.
"""
from flask import Blueprint
from app.controllers.agronomy_aquaculture_water_recirculation_controller import AgronomyAquacultureWaterRecirculationEngineController

agronomy_aquaculture_water_recirculation_bp = Blueprint("agronomy-aquaculture-water-recirculation", __name__, url_prefix="/api/agronomy-aquaculture-water-recirculation")
ctrl = AgronomyAquacultureWaterRecirculationEngineController()

@agronomy_aquaculture_water_recirculation_bp.route("/compute", methods=["POST"])
def compute():
    return ctrl.compute()
