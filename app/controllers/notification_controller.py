"""
Notification Controller Module for Smart Farmer Assistant.

Manages local user notifications, system alerts, irrigation reminders, fertilizer schedules,
disease warnings, financial alerts, mark-as-read status, and notification history.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, redirect, url_for, flash, session, Response
from app.controllers.base_controller import BaseController
from app.services.notification_service import NotificationService
from app.schemas.notification_schema import NotificationSchema
import logging

logger = logging.getLogger(__name__)


class NotificationController(BaseController):
    """
    Controller handling user notification inbox, unread count polling,
    marking alerts read, and notification preference configuration.
    """

    def __init__(self):
        self.notification_service = NotificationService()
        self.notification_schema = NotificationSchema()

    def list_notifications(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists user notifications sorted by timestamp descending.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("auth.login"))

        page, per_page = self.parse_pagination_params()
        filters = self.parse_filter_params()

        notifications, total = self.notification_service.get_notifications_by_user_paginated(user_id, page=page, per_page=per_page, filters=filters)
        unread_count = self.notification_service.get_unread_count(user_id)
        serialized = self.notification_schema.dump_list(notifications)

        if request.is_json or request.path.startswith("/api/"):
            return self.paginated_response(
                items=serialized,
                total=total,
                page=page,
                per_page=per_page,
                message="Notifications retrieved"
            )

        return render_template(
            "farmer/notifications.html",
            notifications=notifications,
            notifications_data=serialized,
            unread_count=unread_count,
            page=page,
            per_page=per_page,
            total=total,
            filters=filters
        )

    def mark_as_read(self, notification_id: int) -> Union[Response, str]:
        """
        Marks a specific notification as read.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        success = self.notification_service.mark_notification_as_read(notification_id, user_id)
        if not success:
            return self.error_response(message="Notification not found", status_code=404)

        if request.is_json:
            return self.success_response(message="Notification marked as read")

        flash("Notification marked as read", "info")
        return redirect(url_for("farmer.list_notifications"))

    def mark_all_as_read(self) -> Union[Response, str]:
        """
        Marks all notifications for the authenticated user as read.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.error_response(message="Authentication required", status_code=401)

        count = self.notification_service.mark_all_read(user_id)
        if request.is_json:
            return self.success_response(data={"count": count}, message=f"Marked {count} notifications as read")

        flash(f"Marked {count} notifications as read.", "success")
        return redirect(url_for("farmer.list_notifications"))

    def get_unread_count(self) -> Tuple[Response, int]:
        """
        REST endpoint returning unread notification count badge number.
        """
        user_id = self.get_current_user_id()
        if not user_id:
            return self.success_response(data={"unread_count": 0})

        count = self.notification_service.get_unread_count(user_id)
        return self.success_response(data={"unread_count": count})
