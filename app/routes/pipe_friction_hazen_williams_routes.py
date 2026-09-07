"""
PipeFrictionHazenWilliamsEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.pipe_friction_hazen_williams_controller import PipeFrictionHazenWilliamsEngineController

pipe_friction_hazen_williams_bp = Blueprint("pipe-friction-hazen-williams", __name__, url_prefix="/api/pipe-friction-hazen-williams")
controller = PipeFrictionHazenWilliamsEngineController()

@pipe_friction_hazen_williams_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@pipe_friction_hazen_williams_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@pipe_friction_hazen_williams_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
