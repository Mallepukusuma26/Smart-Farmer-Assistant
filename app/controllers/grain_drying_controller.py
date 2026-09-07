"""
Grain Drying Controller Module for Smart Farmer Assistant.

Manages Equilibrium Moisture Content (EMC %) Henderson math and post-harvest drying storage suitability.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.grain_drying_service import GrainDryingService
import logging

logger = logging.getLogger(__name__)


class GrainDryingController(BaseController):
    """
    Controller handling Equilibrium Moisture Content (EMC) calculations and safe storage evaluation.
    """

    def __init__(self):
        self.drying_service = GrainDryingService()

    def calculate_emc(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates Equilibrium Moisture Content (EMC %) for grain.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        temp = float(data.get("temperature_c", 25.0))
        rh = float(data.get("relative_humidity_pct", 70.0))
        grain = data.get("grain_type", "rice")

        res = self.drying_service.calculate_modified_henderson_emc(temp, rh, grain)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/grain_drying.html", result=res)
