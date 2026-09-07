"""
IPMPheromoneTrapCatchThresholdEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.ipm_pheromone_trap_catch_threshold_controller import IPMPheromoneTrapCatchThresholdEngineController

ipm_pheromone_trap_catch_threshold_bp = Blueprint("ipm-pheromone-trap-catch-threshold", __name__, url_prefix="/api/ipm-pheromone-trap-catch-threshold")
controller = IPMPheromoneTrapCatchThresholdEngineController()

@ipm_pheromone_trap_catch_threshold_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@ipm_pheromone_trap_catch_threshold_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@ipm_pheromone_trap_catch_threshold_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
