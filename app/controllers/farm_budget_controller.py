"""
Farm Budget Controller Module for Smart Farmer Assistant.

Manages enterprise budget calculations, machinery depreciation schedules, and break-even price matrices.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.farm_budget_service import FarmBudgetService
import logging

logger = logging.getLogger(__name__)


class FarmBudgetController(BaseController):
    """
    Controller handling enterprise budget formulation, asset depreciation math, and break-even matrix generation.
    """

    def __init__(self):
        self.budget_service = FarmBudgetService()

    def generate_budget(self) -> Union[str, Tuple[Response, int]]:
        """
        Generates detailed enterprise budget breakdown and break-even price matrix.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            crop_name = data.get("crop_name", "rice")
            land_area = float(data.get("land_area_acres", 5.0))
            expected_yield = float(data.get("expected_yield_per_acre", 3.0))
            expected_price = float(data.get("expected_market_price_per_tonne", 450.0))

            variable_costs = {
                "seed": float(data.get("seed_cost", 200.0)),
                "fertilizer": float(data.get("fertilizer_cost", 400.0)),
                "pesticide": float(data.get("pesticide_cost", 150.0)),
                "labour": float(data.get("labour_cost", 500.0)),
                "irrigation": float(data.get("irrigation_cost", 250.0))
            }
            fixed_costs = {
                "machinery_depreciation": float(data.get("machinery_depreciation", 300.0)),
                "land_rent": float(data.get("land_rent", 400.0))
            }

            res = self.budget_service.generate_enterprise_budget(
                crop_name=crop_name,
                land_area_acres=land_area,
                variable_costs=variable_costs,
                fixed_costs=fixed_costs,
                expected_yield_per_acre=expected_yield,
                expected_price_per_unit=expected_price
            )

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=res, message="Enterprise budget generated successfully")

            return render_template("farmer/enterprise_budget.html", result=res, form_data=data)

        except Exception as e:
            return self.handle_exception(e, "Error generating enterprise budget")
