"""
Land Survey Controller Module for Smart Farmer Assistant.

Manages Shoelace polygon boundary area calculations, GPS centroid coordinate math, and RUSLE slope ratings.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.land_survey_service import LandSurveyService
import logging

logger = logging.getLogger(__name__)


class LandSurveyController(BaseController):
    """
    Controller handling spatial field boundary area calculations and topographic slope ratings.
    """

    def __init__(self):
        self.survey_service = LandSurveyService()

    def calculate_polygon_area(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates field plot acreage from boundary coordinate polygon points.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        coords = data.get("coordinates", [(77.1025, 28.7041), (77.1035, 28.7041), (77.1035, 28.7051), (77.1025, 28.7051)])

        res = self.survey_service.calculate_shoelace_area_acres(coords)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/land_survey.html", result=res)
