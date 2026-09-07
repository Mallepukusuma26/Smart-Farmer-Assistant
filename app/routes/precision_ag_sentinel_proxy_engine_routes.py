"""
PrecisionAgSentinelProxyEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_sentinel_proxy_engine_controller import PrecisionAgSentinelProxyEngineController

precision_ag_sentinel_proxy_engine_bp = Blueprint("precision-ag-sentinel-proxy-engine", __name__, url_prefix="/api/precision-ag-sentinel-proxy-engine")
controller = PrecisionAgSentinelProxyEngineController()

@precision_ag_sentinel_proxy_engine_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_sentinel_proxy_engine_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_sentinel_proxy_engine_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
