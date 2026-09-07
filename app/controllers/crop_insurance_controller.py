"""
Crop Insurance Controller Module for Smart Farmer Assistant.

Manages Weather-Index Crop Insurance yield loss indemnity calculations and premium subsidies.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.crop_insurance_risk_service import CropInsuranceRiskService
import logging

logger = logging.getLogger(__name__)


class CropInsuranceController(BaseController):
    """
    Controller handling weather-index crop insurance triggers and payout calculations.
    """

    def __init__(self):
        self.insurance_service = CropInsuranceRiskService()

    def calculate_indemnity(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates area-yield crop insurance yield loss payout.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        guaranteed = float(data.get("guaranteed_yield_tonnes_acre", 3.5))
        actual = float(data.get("actual_harvested_yield_tonnes_acre", 2.1))
        sum_insured = float(data.get("sum_insured_usd_acre", 600.0))
        subsidy = float(data.get("subsidy_pct", 50.0))

        res = self.insurance_service.calculate_yield_index_indemnity(guaranteed, actual, sum_insured, subsidy)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/crop_insurance.html", result=res)
