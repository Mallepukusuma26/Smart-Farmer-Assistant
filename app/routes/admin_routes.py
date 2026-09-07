"""
Admin Routes Blueprint for Smart Farmer Assistant.

Maps administration endpoints for global system management, user administration,
crop master list, fertilizer master list, audit trail inspection, ML model monitoring,
and system analytics.
"""

from flask import Blueprint, request
from app.controllers.admin_controller import AdminController
from app.controllers.farmer_controller import FarmerController
from app.controllers.crop_controller import CropController
from app.controllers.fertilizer_controller import FertilizerController
from app.controllers.ml_controller import MLController

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

admin_controller = AdminController()
farmer_controller = FarmerController()
crop_controller = CropController()
fertilizer_controller = FertilizerController()
ml_controller = MLController()


@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return admin_controller.dashboard()


@admin_bp.route("/users", methods=["GET"])
def list_users():
    return admin_controller.list_users()


@admin_bp.route("/users/<int:user_id>/toggle-status", methods=["POST"])
def toggle_user_status(user_id):
    return admin_controller.toggle_user_status(user_id)


@admin_bp.route("/farmers", methods=["GET"])
def list_farmers():
    return farmer_controller.list_farmers()


@admin_bp.route("/crops", methods=["GET", "POST"])
def list_crops():
    if request.method == "GET":
        return crop_controller.list_crops()
    return crop_controller.create_crop()


@admin_bp.route("/fertilizers", methods=["GET", "POST"])
def list_fertilizers():
    if request.method == "GET":
        return fertilizer_controller.list_fertilizers()
    return fertilizer_controller.create_fertilizer()


@admin_bp.route("/ml-models", methods=["GET"])
def ml_models():
    return ml_controller.get_ml_status()


@admin_bp.route("/audit-logs", methods=["GET"])
def audit_logs():
    return admin_controller.audit_logs()
