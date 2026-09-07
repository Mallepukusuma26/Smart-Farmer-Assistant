"""
SafetyPesticideWorkerReentryIntervalEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.safety_pesticide_worker_reentry_interval_controller import SafetyPesticideWorkerReentryIntervalEngineController

safety_pesticide_worker_reentry_interval_bp = Blueprint("safety-pesticide-worker-reentry-interval", __name__, url_prefix="/api/safety-pesticide-worker-reentry-interval")
controller = SafetyPesticideWorkerReentryIntervalEngineController()

@safety_pesticide_worker_reentry_interval_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@safety_pesticide_worker_reentry_interval_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@safety_pesticide_worker_reentry_interval_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
