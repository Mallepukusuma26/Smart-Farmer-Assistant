"""
IPMBiologicalControlParasitoidRatioEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.ipm_biological_control_parasitoid_ratio_controller import IPMBiologicalControlParasitoidRatioEngineController

ipm_biological_control_parasitoid_ratio_bp = Blueprint("ipm-biological-control-parasitoid-ratio", __name__, url_prefix="/api/ipm-biological-control-parasitoid-ratio")
controller = IPMBiologicalControlParasitoidRatioEngineController()

@ipm_biological_control_parasitoid_ratio_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@ipm_biological_control_parasitoid_ratio_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@ipm_biological_control_parasitoid_ratio_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
