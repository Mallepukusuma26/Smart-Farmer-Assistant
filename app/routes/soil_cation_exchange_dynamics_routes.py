"""
SoilCationExchangeDynamicsEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_cation_exchange_dynamics_controller import SoilCationExchangeDynamicsEngineController

soil_cation_exchange_dynamics_bp = Blueprint("soil-cation-exchange-dynamics", __name__, url_prefix="/api/soil-cation-exchange-dynamics")
controller = SoilCationExchangeDynamicsEngineController()

@soil_cation_exchange_dynamics_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_cation_exchange_dynamics_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_cation_exchange_dynamics_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
