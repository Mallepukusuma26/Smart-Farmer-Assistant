"""
Admin Controller Module for Smart Farmer Assistant.

Manages system administration, user roles, system audit logs, dataset status,
ML model performance monitoring, system settings, database backups, and security log review.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.user_service import UserService
from app.services.audit_service import AuditService
from app.services.dashboard_service import DashboardService
from app.schemas.user_schema import UserSchema
from app.schemas.audit_schema import AuditSchema
import logging

logger = logging.getLogger(__name__)


class AdminController(BaseController):
    """
    Controller handling system administration tasks, audit trail inspection,
    user activation/deactivation, role assignment, system setting configuration,
    and platform stats monitoring.
    """

    def __init__(self):
        self.user_service = UserService()
        self.audit_service = AuditService()
        self.dashboard_service = DashboardService()
        self.user_schema = UserSchema()
        self.audit_schema = AuditSchema()

    def dashboard(self) -> Union[str, Tuple[Response, int]]:
        """
        Renders the main Admin Control Center dashboard.
        """
        if not self.is_admin():
            if self.is_authenticated():
                return render_template("errors/403.html"), 403
            return redirect(url_for("auth.login"))


        analytics = self.dashboard_service.get_admin_dashboard_analytics()
        recent_audits = self.audit_service.get_recent_audit_logs(limit=10)

        context = {
            "analytics": analytics,
            "recent_audits": self.audit_schema.dump_list(recent_audits)
        }

        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=context)

        return render_template("admin/dashboard.html", **context)

    def list_users(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists all registered platform users with role filtering, status filters, and search.
        """
        if not self.is_admin():
            return self.error_response(message="Admin access required", status_code=403)

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        users, total = self.user_service.get_users_paginated(page=page, per_page=per_page, filters=filters)
        serialized = self.user_schema.dump_list(users)

        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "admin/users.html",
            users=users,
            users_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def toggle_user_status(self, user_id: int) -> Union[Response, str]:
        """
        Activates or deactivates a user account.
        """
        if not self.is_admin():
            return self.error_response(message="Admin access required", status_code=403)

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return self.error_response(message="User not found", status_code=404)

        if user.id == self.get_current_user_id():
            return self.error_response(message="Cannot deactivate your own admin account", status_code=400)

        updated_user = self.user_service.toggle_user_active_status(user_id)
        status_str = "activated" if updated_user.is_active else "deactivated"

        self.audit_service.log_event(
            user_id=self.get_current_user_id(),
            action=f"USER_{status_str.upper()}",
            entity_type="User",
            entity_id=user_id,
            details={"target_username": user.username}
        )

        if request.is_json:
            return self.success_response(
                data=self.user_schema.dump_single(updated_user),
                message=f"User {user.username} {status_str} successfully"
            )

        flash(f"User {user.username} {status_str} successfully", "success")
        return redirect(url_for("admin.list_users"))

    def audit_logs(self) -> Union[str, Tuple[Response, int]]:
        """
        Renders system audit log history with action type and user filters.
        """
        if not self.is_admin():
            return self.error_response(message="Admin access required", status_code=403)

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        logs, total = self.audit_service.get_audit_logs_paginated(page=page, per_page=per_page, filters=filters)
        serialized = self.audit_schema.dump_list(logs)

        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(items=serialized, total=total, page=page, per_page=per_page)

        return render_template(
            "admin/audit_logs.html",
            logs=logs,
            logs_data=serialized,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )
