"""
Fertilizer Blending Controller Module for Smart Farmer Assistant.

Manages physical fertilizer blending formulations (Urea, DAP, MOP) to achieve custom NPK nutrient grades.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.fertilizer_blending_service import FertilizerBlendingService
import logging

logger = logging.getLogger(__name__)


class FertilizerBlendingController(BaseController):
    """
    Controller handling custom NPK physical fertilizer blending math.
    """

    def __init__(self):
        self.blending_service = FertilizerBlendingService()

    def calculate_blend(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates required weights of Urea, DAP, and MOP to satisfy target N-P-K nutrient weights.
        """
        if request.method == "GET":
            return render_template("farmer/fertilizer_blend.html")

        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            target_n = float(data.get("nitrogen_kg", 50.0))
            target_p = float(data.get("phosphorus_kg", 30.0))
            target_k = float(data.get("potassium_kg", 40.0))

            res = self.blending_service.calculate_custom_blend(
                target_n_kg=target_n,
                target_p_kg=target_p,
                target_k_kg=target_k
            )

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=res, message="Fertilizer blend formulation generated")

            return render_template("farmer/fertilizer_blend.html", result=res, form_data=data)

        except Exception as e:
            return self.handle_exception(e, "Error calculating fertilizer blend formulation")
