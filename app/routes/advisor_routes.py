"""
Advisor Routes Blueprint for Smart Farmer Assistant.

Maps endpoints for agricultural advisor portal, farmer case assignment, consultation advice,
field visit logs, and expert consultation history.
"""

from flask import Blueprint, request
from app.controllers.advisor_controller import AdvisorController
from app.controllers.farmer_controller import FarmerController

advisor_bp = Blueprint("advisor", __name__, url_prefix="/advisor")

advisor_controller = AdvisorController()
farmer_controller = FarmerController()


@advisor_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return advisor_controller.dashboard()


@advisor_bp.route("/cases", methods=["GET", "POST"])
def list_cases():
    if request.method == "GET":
        return advisor_controller.list_cases()
    return advisor_controller.create_case()


@advisor_bp.route("/cases/<int:case_id>/resolve", methods=["POST"])
def resolve_case(case_id):
    return advisor_controller.resolve_case(case_id)


@advisor_bp.route("/farmer/<int:farmer_id>", methods=["GET"])
def farmer_detail(farmer_id):
    return farmer_controller.get_farmer_detail(farmer_id)
