"""
Soil Salinity Controller Module for Smart Farmer Assistant.

Manages Sodium Adsorption Ratio (SAR) and FAO Leaching Requirement (LR %) calculations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.soil_salinity_reclamation_service import SoilSalinityReclamationService
import logging

logger = logging.getLogger(__name__)


class SoilSalinityController(BaseController):
    """
    Controller handling soil sodicity SAR and leaching requirement math.
    """

    def __init__(self):
        self.salinity_service = SoilSalinityReclamationService()

    def calculate_sar(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates Sodium Adsorption Ratio (SAR).
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        na = float(data.get("sodium_meq", 6.0))
        ca = float(data.get("calcium_meq", 3.0))
        mg = float(data.get("magnesium_meq", 2.0))

        res = self.salinity_service.calculate_sodium_adsorption_ratio(na, ca, mg)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/soil_salinity.html", result=res)
