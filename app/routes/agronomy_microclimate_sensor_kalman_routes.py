"""
AgronomyMicroclimateSensorKalmanEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.agronomy_microclimate_sensor_kalman_controller import AgronomyMicroclimateSensorKalmanEngineController

agronomy_microclimate_sensor_kalman_bp = Blueprint("agronomy-microclimate-sensor-kalman", __name__, url_prefix="/api/agronomy-microclimate-sensor-kalman")
controller = AgronomyMicroclimateSensorKalmanEngineController()

@agronomy_microclimate_sensor_kalman_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@agronomy_microclimate_sensor_kalman_bp.route("/evaluate-grid", methods=["POST"])
def evaluate_grid():
    return controller.evaluate_grid()
