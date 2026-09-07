"""
Crop Health Controller Module for Smart Farmer Assistant.

Manages Crop Health Index (CHI) evaluation, SPAD chlorophyll ratings, and abiotic stress diagnosis.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.crop_health_service import CropHealthService
import logging

logger = logging.getLogger(__name__)


class CropHealthController(BaseController):
    """
    Controller handling Crop Health Index calculations and stress diagnosis.
    """

    def __init__(self):
        self.health_service = CropHealthService()

    def evaluate_health(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates Crop Health Index (CHI) from SPAD, LAI, and canopy cover inputs.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        spad = float(data.get("spad_chlorophyll", 42.0))
        canopy = float(data.get("canopy_cover_pct", 75.0))
        lai = float(data.get("leaf_area_index_lai", 3.5))
        stress = float(data.get("water_stress_index", 0.1))

        res = self.health_service.calculate_crop_health_index(spad, canopy, lai, stress)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/crop_health.html", result=res)
