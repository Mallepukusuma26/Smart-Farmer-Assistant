"""
OrganicCertificationComplianceCostEngine Routes Blueprint.
"""

from flask import Blueprint
from app.controllers.organic_certification_compliance_cost_controller import OrganicCertificationComplianceCostEngineController

organic_certification_compliance_cost_bp = Blueprint("organic-certification-compliance-cost", __name__, url_prefix="/api/organic-certification-compliance-cost")
controller = OrganicCertificationComplianceCostEngineController()

@organic_certification_compliance_cost_bp.route("/compute", methods=["POST"])
def compute():
    return controller.compute_metric()

@organic_certification_compliance_cost_bp.route("/simulate", methods=["POST"])
def simulate():
    return controller.run_simulation()

@organic_certification_compliance_cost_bp.route("/calibrate", methods=["POST"])
def calibrate():
    return controller.calibrate()
