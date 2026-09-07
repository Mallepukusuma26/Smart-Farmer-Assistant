"""
Soil Fertility Controller Module for Smart Farmer Assistant.

Manages DTPA micronutrient evaluation (Zn, Fe, Cu, Mn, B) and CEC cation exchange capacity calculations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.soil_fertility_index_service import SoilFertilityIndexService
import logging

logger = logging.getLogger(__name__)


class SoilFertilityController(BaseController):
    """
    Controller handling soil micronutrient sufficiency ratings and base saturation calculations.
    """

    def __init__(self):
        self.fertility_service = SoilFertilityIndexService()

    def evaluate_micronutrients(self) -> Union[str, Tuple[Response, int]]:
        """
        Evaluates soil DTPA micronutrients against critical limits.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        zn = float(data.get("zinc", 0.5))
        fe = float(data.get("iron", 4.0))
        cu = float(data.get("copper", 0.3))
        mn = float(data.get("manganese", 2.5))
        b = float(data.get("boron", 0.4))

        res = self.fertility_service.evaluate_micronutrients(zn, fe, cu, mn, b)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/soil_fertility.html", result=res)
