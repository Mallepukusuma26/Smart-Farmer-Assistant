"""
PrecisionAgYieldMonitorDataCleanerEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.precision_ag_yield_monitor_data_cleaner_controller import PrecisionAgYieldMonitorDataCleanerEngineController

precision_ag_yield_monitor_data_cleaner_bp = Blueprint("precision-ag-yield-monitor-data-cleaner", __name__, url_prefix="/api/precision-ag-yield-monitor-data-cleaner")
controller = PrecisionAgYieldMonitorDataCleanerEngineController()

@precision_ag_yield_monitor_data_cleaner_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@precision_ag_yield_monitor_data_cleaner_bp.route("/analyze-grid", methods=["POST"])
def analyze_grid():
    return controller.analyze_grid()

@precision_ag_yield_monitor_data_cleaner_bp.route("/report", methods=["GET"])
def get_report():
    return controller.get_report()
