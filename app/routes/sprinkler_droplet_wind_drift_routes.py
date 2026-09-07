"""
SprinklerDropletWindDriftEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.sprinkler_droplet_wind_drift_controller import SprinklerDropletWindDriftEngineController

sprinkler_droplet_wind_drift_bp = Blueprint("sprinkler-droplet-wind-drift", __name__, url_prefix="/api/sprinkler-droplet-wind-drift")
controller = SprinklerDropletWindDriftEngineController()

@sprinkler_droplet_wind_drift_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@sprinkler_droplet_wind_drift_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@sprinkler_droplet_wind_drift_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
