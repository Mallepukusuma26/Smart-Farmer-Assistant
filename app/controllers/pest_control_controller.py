"""
Pest Control Controller Module for Smart Farmer Assistant.

Manages Integrated Pest Management (IPM) protocols, Economic Injury Level (EIL) calculations, and PHI waiting periods.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.pest_control_service import PestControlService
import logging

logger = logging.getLogger(__name__)


class PestControlController(BaseController):
    """
    Controller handling IPM recommendations, EIL math, and spray schedule generation.
    """

    def __init__(self):
        self.pest_service = PestControlService()

    def get_ipm_recommendation(self) -> Union[str, Tuple[Response, int]]:
        """
        Retrieves IPM protocol and pesticide dosage for selected pest.
        """
        pest_name = request.args.get("pest_name", request.form.get("pest_name", "stem borer"))
        area = float(request.args.get("area_acres", request.form.get("area_acres", 1.0)))

        res = self.pest_service.get_ipm_recommendation(pest_name=pest_name, area_acres=area)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/pest_control.html", result=res)
