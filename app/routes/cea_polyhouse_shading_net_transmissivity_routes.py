"""
CEAPolyhouseShadingNetTransmissivityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.cea_polyhouse_shading_net_transmissivity_controller import CEAPolyhouseShadingNetTransmissivityEngineController

cea_polyhouse_shading_net_transmissivity_bp = Blueprint("cea-polyhouse-shading-net-transmissivity", __name__, url_prefix="/api/cea-polyhouse-shading-net-transmissivity")
controller = CEAPolyhouseShadingNetTransmissivityEngineController()

@cea_polyhouse_shading_net_transmissivity_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@cea_polyhouse_shading_net_transmissivity_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@cea_polyhouse_shading_net_transmissivity_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
