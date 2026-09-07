"""
Authentication Routes Blueprint for Smart Farmer Assistant.

Maps endpoints for user registration, login authentication, logout, profile settings,
password change, and password reset workflows.
"""

from flask import Blueprint, request
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_controller = AuthController()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return auth_controller.register()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return auth_controller.login()


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    return auth_controller.logout()


@auth_bp.route("/profile", methods=["GET", "POST"])
def profile():
    return auth_controller.profile()


@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    return auth_controller.change_password()


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def reset_password_request():
    return auth_controller.reset_password_request()
