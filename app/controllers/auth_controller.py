"""
Authentication and Authorization Controller Module for Smart Farmer Assistant.

Manages user registration, login, logout, password reset workflow, profile updating,
role switching, account activation/deactivation, and login activity tracking.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.farmer_service import FarmerService
from app.services.advisor_service import AdvisorService
from app.services.audit_service import AuditService
from app.validators.auth_validator import AuthValidator
from app.schemas.user_schema import UserSchema
import logging

logger = logging.getLogger(__name__)


class AuthController(BaseController):
    """
    Handles user authentication lifecycle: registration, login authentication,
    session initialization, password changes, password reset requests, role verification,
    and profile data management.
    """

    def __init__(self):
        self.auth_service = AuthService()
        self.user_service = UserService()
        self.farmer_service = FarmerService()
        self.advisor_service = AdvisorService()
        self.audit_service = AuditService()
        self.auth_validator = AuthValidator()
        self.user_schema = UserSchema()

    def register(self) -> Union[str, Tuple[Response, int]]:
        """
        Processes new user registration for Farmers, Advisors, and Admins.
        Validates input schema, hashes password, creates user account, initializes role profile,
        and logs audit trail.
        """
        if request.method == "GET":
            if self.is_authenticated():
                return self._redirect_dashboard_by_role(session.get("role"))
            return render_template("auth/register.html")

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.auth_validator.validate_registration(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Registration validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return render_template("auth/register.html", form_data=data, errors=validation_errors), 400

        try:
            username = data.get("username", "").strip()
            email = data.get("email", "").strip().lower()
            password = data.get("password")
            role = data.get("role", "farmer").strip().lower()
            full_name = data.get("full_name", "").strip()
            phone = data.get("phone", "").strip()
            address = data.get("address", "").strip()

            user = self.auth_service.register_user(
                username=username,
                email=email,
                password=password,
                role=role,
                full_name=full_name,
                phone=phone,
                address=address
            )

            if not user:
                msg = "User registration failed. Email or username may already be in use."
                if request.is_json:
                    return self.error_response(message=msg, status_code=400)
                flash(msg, "danger")
                return render_template("auth/register.html", form_data=data), 400

            # Audit log
            role_val = user.role.value if hasattr(user.role, 'value') else str(user.role)
            self.audit_service.log_event(
                user_id=user.id,
                action="USER_REGISTERED",
                entity_type="User",
                entity_id=user.id,
                details={"username": user.username, "email": user.email, "role": role_val}
            )

            # Auto login upon registration
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            session["email"] = user.email
            session["role"] = role_val
            session["full_name"] = user.full_name or user.username

            if request.is_json:
                user_data = self.user_schema.dump_single(user)
                return self.success_response(
                    data={"user": user_data, "redirect_url": self._get_dashboard_url(role_val)},
                    message="Registration successful! Welcome to Smart Farmer Assistant.",
                    status_code=201
                )

            flash("Registration successful! Welcome to Smart Farmer Assistant.", "success")
            return redirect(self._get_dashboard_url(role_val))

        except Exception as e:
            return self.handle_exception(e, "Error processing registration")

    def login(self) -> Union[str, Tuple[Response, int]]:
        """
        Authenticates user credentials, sets session security context, updates login timestamp,
        and redirects user to role-specific dashboard.
        """
        if request.method == "GET":
            if self.is_authenticated():
                return self._redirect_dashboard_by_role(session.get("role"))
            return render_template("auth/login.html")

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.auth_validator.validate_login(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Login validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(str(err), "danger")
            return render_template("auth/login.html", errors=validation_errors), 200

        try:
            username_or_email = (data.get("username_or_email") or data.get("username") or data.get("email") or "").strip()
            password = data.get("password")

            user, token = self.auth_service.authenticate_user(username_or_email, password)
            if not user:
                msg = "Invalid credentials. Please check your username/email and password."

                if request.is_json:
                    return self.error_response(message=msg, status_code=401)
                flash(msg, "danger")
                return render_template("auth/login.html"), 200

            if not user.is_active:
                msg = "Your account has been deactivated. Please contact support or system administrator."
                if request.is_json:
                    return self.error_response(message=msg, status_code=403)
                flash(msg, "warning")
                return render_template("auth/login.html"), 403

            # Session initialization
            role_val = user.role.value if hasattr(user.role, 'value') else str(user.role)
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            session["email"] = user.email
            session["role"] = role_val
            session["full_name"] = getattr(user, 'full_name', None) or user.username

            self.audit_service.log_event(
                user_id=user.id,
                action="USER_LOGIN",
                entity_type="User",
                entity_id=user.id,
                details={"ip_address": request.remote_addr, "user_agent": request.headers.get("User-Agent", "")}
            )

            redirect_url = self._get_dashboard_url(role_val)
            if request.is_json:
                user_data = self.user_schema.dump_single(user)
                return self.success_response(
                    data={"user": user_data, "token": token, "redirect_url": redirect_url},
                    message="Login successful"
                )

            user_name = getattr(user, 'full_name', None) or user.username
            flash(f"Welcome back, {user_name}!", "success")
            return redirect(redirect_url)

        except Exception as e:
            return self.handle_exception(e, "Error processing login")

    def logout(self) -> Union[Response, str]:
        """
        Clears authentication session, records logout audit entry, and redirects to login page.
        """
        user_id = self.get_current_user_id()
        if user_id:
            self.audit_service.log_event(
                user_id=user_id,
                action="USER_LOGOUT",
                entity_type="User",
                entity_id=user_id
            )
        session.clear()

        if request.is_json:
            return self.success_response(message="Logged out successfully")

        flash("You have been logged out.", "info")
        return redirect(url_for("auth.login"))

    def profile(self) -> Union[str, Tuple[Response, int]]:
        """
        Renders user profile details or updates personal contact and preferences data.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return self.error_response(message="User not found", status_code=404)

        if request.method == "GET":
            user_data = self.user_schema.dump_single(user)
            if request.is_json:
                return self.success_response(data=user_data)
            return render_template("auth/profile.html", user=user, user_data=user_data)

        data = request.get_json() if request.is_json else request.form.to_dict()
        is_valid, validation_errors = self.auth_validator.validate_profile_update(data)
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Profile validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return render_template("auth/profile.html", user=user, errors=validation_errors), 400

        try:
            updated_user = self.user_service.update_user_profile(user_id, data)
            if updated_user:
                session["full_name"] = updated_user.full_name or updated_user.username
                self.audit_service.log_event(
                    user_id=user_id,
                    action="PROFILE_UPDATED",
                    entity_type="User",
                    entity_id=user_id
                )

            if request.is_json:
                return self.success_response(
                    data=self.user_schema.dump_single(updated_user),
                    message="Profile updated successfully"
                )

            flash("Profile updated successfully", "success")
            return redirect(url_for("auth.profile"))

        except Exception as e:
            return self.handle_exception(e, "Error updating profile")

    def change_password(self) -> Union[str, Tuple[Response, int]]:
        """
        Validates current password and updates password credentials with secure hash.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        data = request.get_json() if request.is_json else request.form.to_dict()
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        is_valid, validation_errors = self.auth_validator.validate_password_change(
            current_password, new_password, confirm_password
        )
        if not is_valid:
            if request.is_json:
                return self.error_response(message="Password validation failed", errors=validation_errors, status_code=400)
            for err in validation_errors:
                flash(err, "danger")
            return redirect(url_for("auth.profile"))

        try:
            success, msg = self.auth_service.change_password(user_id, current_password, new_password)
            if not success:
                if request.is_json:
                    return self.error_response(message=msg, status_code=400)
                flash(msg, "danger")
                return redirect(url_for("auth.profile"))

            self.audit_service.log_event(
                user_id=user_id,
                action="PASSWORD_CHANGED",
                entity_type="User",
                entity_id=user_id
            )

            if request.is_json:
                return self.success_response(message="Password changed successfully")

            flash("Password changed successfully", "success")
            return redirect(url_for("auth.profile"))

        except Exception as e:
            return self.handle_exception(e, "Error changing password")

    def reset_password_request(self) -> Union[str, Tuple[Response, int]]:
        """
        Generates local offline password reset token for account recovery.
        """
        if request.method == "GET":
            return render_template("auth/forgot_password.html")

        data = request.get_json() if request.is_json else request.form.to_dict()
        email = data.get("email", "").strip().lower()

        if not email:
            msg = "Email address is required"
            if request.is_json:
                return self.error_response(message=msg, status_code=400)
            flash(msg, "danger")
            return render_template("auth/forgot_password.html"), 400

        reset_token = self.auth_service.generate_reset_token(email)
        msg = "If your email is registered, password reset instructions have been generated."

        if request.is_json:
            return self.success_response(data={"reset_token": reset_token}, message=msg)

        flash(msg, "info")
        return render_template("auth/forgot_password.html", reset_token=reset_token)

    def _get_dashboard_url(self, role: str) -> str:
        """
        Returns the appropriate dashboard route URL depending on user role.
        """
        r = str(role).lower()
        if r in ["admin"]:
            return url_for("admin.dashboard")
        elif r in ["advisor"]:
            return url_for("advisor.dashboard")
        return url_for("farmer.dashboard")

    def _redirect_dashboard_by_role(self, role: str) -> Response:
        """
        Redirects to the dashboard corresponding to user role.
        """
        return redirect(self._get_dashboard_url(role))
