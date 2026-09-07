"""
IrrigationDeficitRegulatedRDIEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.irrigation_deficit_regulated_rdi_controller import IrrigationDeficitRegulatedRDIEngineController

irrigation_deficit_regulated_rdi_bp = Blueprint("irrigation-deficit-regulated-rdi", __name__, url_prefix="/api/irrigation-deficit-regulated-rdi")
controller = IrrigationDeficitRegulatedRDIEngineController()

@irrigation_deficit_regulated_rdi_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@irrigation_deficit_regulated_rdi_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@irrigation_deficit_regulated_rdi_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
