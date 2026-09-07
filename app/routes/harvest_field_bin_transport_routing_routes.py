"""
HarvestFieldBinTransportRoutingEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.harvest_field_bin_transport_routing_controller import HarvestFieldBinTransportRoutingEngineController

harvest_field_bin_transport_routing_bp = Blueprint("harvest-field-bin-transport-routing", __name__, url_prefix="/api/harvest-field-bin-transport-routing")
controller = HarvestFieldBinTransportRoutingEngineController()

@harvest_field_bin_transport_routing_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute()

@harvest_field_bin_transport_routing_bp.route("/process-grid", methods=["POST"])
def process_grid():
    return controller.process_grid()

@harvest_field_bin_transport_routing_bp.route("/summary", methods=["GET"])
def summary():
    return controller.summary()
