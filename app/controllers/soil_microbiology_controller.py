"""
Soil Microbiology Controller Module for Smart Farmer Assistant.

Manages microbial biomass C:N ratio calculations and soil extracellular enzyme activity evaluations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.soil_microbiology_service import SoilMicrobiologyService
import logging

logger = logging.getLogger(__name__)


class SoilMicrobiologyController(BaseController):
    """
    Controller handling soil biological health indices and microbial biomass evaluations.
    """

    def __init__(self):
        self.bio_service = SoilMicrobiologyService()

    def evaluate_biomass(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates microbial biomass C:N ratio.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        mc = float(data.get("microbial_carbon", 250.0))
        mn = float(data.get("microbial_nitrogen", 25.0))

        res = self.bio_service.calculate_microbial_biomass_cn(mc, mn)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/soil_microbiology.html", result=res)
