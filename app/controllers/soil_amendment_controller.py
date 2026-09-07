"""
Soil Amendment Controller Module for Smart Farmer Assistant.

Manages chemical and organic soil amendment calculations (agricultural lime, gypsum, elemental sulfur).
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.soil_amendment_service import SoilAmendmentService
import logging

logger = logging.getLogger(__name__)


class SoilAmendmentController(BaseController):
    """
    Controller handling lime and gypsum requirement calculations for soil health remediation.
    """

    def __init__(self):
        self.amendment_service = SoilAmendmentService()

    def calculate_lime(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates agricultural lime dosage required for acidic soils.
        """
        if request.method == "GET":
            return render_template("farmer/soil_amendment.html")

        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            current_ph = float(data.get("current_ph", 5.2))
            target_ph = float(data.get("target_ph", 6.5))
            soil_type = data.get("soil_type", "Loam")
            area_acres = float(data.get("area_acres", 1.0))

            res = self.amendment_service.calculate_lime_requirement(
                current_ph=current_ph,
                target_ph=target_ph,
                soil_type=soil_type,
                area_acres=area_acres
            )

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=res, message="Lime requirement calculated successfully")

            return render_template("farmer/soil_amendment.html", result=res, form_data=data)

        except Exception as e:
            return self.handle_exception(e, "Error calculating lime requirement")

    def calculate_gypsum(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates Gypsum dosage required for sodic soil reclamation.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            esp_pct = float(data.get("esp_pct", 18.0))
            target_esp_pct = float(data.get("target_esp_pct", 5.0))
            cec = float(data.get("cec", 20.0))
            area_acres = float(data.get("area_acres", 1.0))

            res = self.amendment_service.calculate_gypsum_requirement(
                esp_pct=esp_pct,
                target_esp_pct=target_esp_pct,
                cec_meq_100g=cec,
                area_acres=area_acres
            )

            return self.success_response(data=res, message="Gypsum requirement calculated successfully")

        except Exception as e:
            return self.handle_exception(e, "Error calculating gypsum requirement")
