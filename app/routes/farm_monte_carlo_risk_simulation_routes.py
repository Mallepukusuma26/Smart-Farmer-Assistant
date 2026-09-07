"""
FarmMonteCarloRiskSimulationEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.farm_monte_carlo_risk_simulation_controller import FarmMonteCarloRiskSimulationEngineController

farm_monte_carlo_risk_simulation_bp = Blueprint("farm-monte-carlo-risk-simulation", __name__, url_prefix="/api/farm-monte-carlo-risk-simulation")
controller = FarmMonteCarloRiskSimulationEngineController()

@farm_monte_carlo_risk_simulation_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@farm_monte_carlo_risk_simulation_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@farm_monte_carlo_risk_simulation_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
