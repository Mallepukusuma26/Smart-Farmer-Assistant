"""
SoilTraceElementBioavailabilityEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.soil_trace_element_bioavailability_controller import SoilTraceElementBioavailabilityEngineController

soil_trace_element_bioavailability_bp = Blueprint("soil-trace-element-bioavailability", __name__, url_prefix="/api/soil-trace-element-bioavailability")
controller = SoilTraceElementBioavailabilityEngineController()

@soil_trace_element_bioavailability_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@soil_trace_element_bioavailability_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@soil_trace_element_bioavailability_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
