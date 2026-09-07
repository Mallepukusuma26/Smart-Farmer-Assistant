"""
Harvest Analytics Controller Module for Smart Farmer Assistant.

Manages grain moisture shrinkage calculations and combine mechanical harvest loss evaluations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.harvest_analytics_service import HarvestAnalyticsService
import logging

logger = logging.getLogger(__name__)


class HarvestAnalyticsController(BaseController):
    """
    Controller handling moisture shrinkage weight discounts and combine harvester loss estimation.
    """

    def __init__(self):
        self.harvest_service = HarvestAnalyticsService()

    def calculate_shrinkage(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates grain weight loss due to drying to target market moisture.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        weight = float(data.get("initial_weight_kg", 5000.0))
        initial_m = float(data.get("initial_moisture_pct", 18.0))
        target_m = float(data.get("target_moisture_pct", 14.0))

        res = self.harvest_service.calculate_moisture_shrinkage(weight, initial_m, target_m)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/harvest_analytics.html", result=res)
