"""
Financial Ratios Controller Module for Smart Farmer Assistant.

Manages Farm Financial Standards Council (FFSC) liquidity, solvency, and profitability ratio evaluations.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.farm_financial_ratios_service import FarmFinancialRatiosService
import logging

logger = logging.getLogger(__name__)


class FinancialRatiosController(BaseController):
    """
    Controller handling FFSC financial ratio evaluations.
    """

    def __init__(self):
        self.ffsc_service = FarmFinancialRatiosService()

    def evaluate_ffsc(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates FFSC liquidity, solvency, and profitability ratios.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        ca = float(data.get("current_assets", 50000.0))
        cl = float(data.get("current_liabilities", 25000.0))
        ta = float(data.get("total_assets", 250000.0))
        tl = float(data.get("total_liabilities", 75000.0))
        rev = float(data.get("gross_revenue", 120000.0))
        exp = float(data.get("operating_expenses", 80000.0))
        nfi = float(data.get("net_farm_income", 40000.0))

        res = self.ffsc_service.calculate_ffsc_ratios(ca, cl, ta, tl, rev, exp, nfi)
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=res)

        return render_template("farmer/financial_ratios.html", result=res)
