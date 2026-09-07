"""
Fertilizer Fertigation Controller Module for Smart Farmer Assistant.

Manages dual-tank A/B drip fertigation recipe calculations and EC target math.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.fertilizer_fertigation_service import FertilizerFertigationService
import logging

logger = logging.getLogger(__name__)


class FertilizerFertigationController(BaseController):
    """
    Controller handling stock solution recipe formulation and fertigation EC targets.
    """

    def __init__(self):
        self.fertigation_service = FertilizerFertigationService()

    def calculate_recipe(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates dual-tank A/B fertigation stock solution recipe.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        vol = float(data.get("volume_liters", 1000.0))
        ec = float(data.get("target_ec", 2.0))
        crop = data.get("crop_type", "tomato")

        res = self.fertigation_service.calculate_fertigation_recipe(vol, ec, crop)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/fertigation_recipe.html", result=res)
