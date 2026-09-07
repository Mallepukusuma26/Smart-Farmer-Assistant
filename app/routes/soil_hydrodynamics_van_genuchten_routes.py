"""
SoilHydrodynamicsVanGenuchtenEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_hydrodynamics_van_genuchten_controller import SoilHydrodynamicsVanGenuchtenEngineController

soil_hydrodynamics_van_genuchten_bp = Blueprint("soil-hydrodynamics-van-genuchten", __name__, url_prefix="/api/soil-hydrodynamics-van-genuchten")
controller = SoilHydrodynamicsVanGenuchtenEngineController()

@soil_hydrodynamics_van_genuchten_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_hydrodynamics_van_genuchten_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_hydrodynamics_van_genuchten_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
