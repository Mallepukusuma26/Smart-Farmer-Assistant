"""
Farm Machinery Cost Controller Module for Smart Farmer Assistant.

Manages Effective Field Capacity (EFC) and tractor diesel fuel consumption calculations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.farm_machinery_cost_service import FarmMachineryCostService
import logging

logger = logging.getLogger(__name__)


class FarmMachineryCostController(BaseController):
    """
    Controller handling machinery operating capacity and diesel fuel economics.
    """

    def __init__(self):
        self.machinery_cost_service = FarmMachineryCostService()

    def calculate_capacity(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates Effective Field Capacity (EFC in Acres/Hour).
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        width = float(data.get("width_meters", 3.0))
        speed = float(data.get("speed_kmh", 6.0))
        eff = float(data.get("efficiency_pct", 80.0))

        res = self.machinery_cost_service.calculate_effective_field_capacity(width, speed, eff)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/machinery_cost.html", result=res)
