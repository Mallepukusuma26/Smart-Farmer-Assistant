"""
Dashboard Controller Module for Smart Farmer Assistant.

Computes system-wide analytics, total farm/field counts, active crop area, financial income/expenses,
soil health averages, disease incident alerts, yield performance, and monthly/seasonal trends.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.dashboard_service import DashboardService
import logging

logger = logging.getLogger(__name__)


class DashboardController(BaseController):
    """
    Controller aggregating real-time analytics for Farmer, Admin, and Advisor dashboards.
    """

    def __init__(self):
        self.dashboard_service = DashboardService()

    def get_farmer_analytics(self) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves analytical metrics and charting datasets for the farmer dashboard.
        """
        user_id = BaseController.get_current_user_id()
        if not user_id:
            return BaseController.error_response(message="Authentication required", status_code=401)

        dashboard_service = DashboardService()
        analytics = dashboard_service.get_farmer_dashboard_analytics(user_id)

        if request.is_json or request.path.startswith("/api/"):
            return BaseController.success_response(data=analytics)

        return render_template("farmer/dashboard.html", analytics=analytics)

    def get_admin_analytics(self) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves global system metrics, user growth charts, disease frequency, and ML model status.
        """
        if not self.is_admin():
            return self.error_response(message="Admin access required", status_code=403)

        analytics = self.dashboard_service.get_admin_dashboard_analytics()

        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=analytics)

        return render_template("admin/dashboard.html", analytics=analytics)
