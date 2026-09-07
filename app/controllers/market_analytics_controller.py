"""
Market Analytics Controller Module for Smart Farmer Assistant.

Manages commodity market price tracking, grain storage trade-off calculations, and regional market mandi rates.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response
from app.controllers.base_controller import BaseController
from app.services.market_price_service import MarketPriceService
from app.services.crop_market_analytics_service import CropMarketAnalyticsService
import logging

logger = logging.getLogger(__name__)


class MarketAnalyticsController(BaseController):
    """
    Controller handling market price trends, grain storage holding economic trade-offs, and mandi prices.
    """

    def __init__(self):
        self.market_service = MarketPriceService()
        self.analytics_service = CropMarketAnalyticsService()

    def get_market_prices(self) -> Union[str, Tuple[Response, int]]:
        """
        Lists tracked commodity market prices and MSP rates.
        """
        prices = self.market_service.get_all_market_prices()
        if request.is_json or request.path.startswith("/api/"):
            return self.success_response(data=prices)
        return render_template("farmer/market_prices.html", prices=prices)

    def calculate_storage_tradeoff(self) -> Union[str, Tuple[Response, int]]:
        """
        Calculates net economic gain/loss of storing harvested grain vs immediate sale.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()
        try:
            current_price = float(data.get("current_price_per_tonne", 450.0))
            future_price = float(data.get("expected_future_price_per_tonne", 520.0))
            quantity = float(data.get("quantity_tonnes", 10.0))
            storage_fee = float(data.get("storage_cost_per_tonne_month", 5.0))
            months = int(data.get("holding_months", 3))

            res = self.analytics_service.calculate_storage_tradeoff(
                current_price_per_tonne=current_price,
                expected_future_price_per_tonne=future_price,
                quantity_tonnes=quantity,
                storage_cost_per_tonne_month=storage_fee,
                holding_months=months
            )

            if request.is_json or request.path.startswith("/api/"):
                return self.success_response(data=res, message="Storage trade-off calculated successfully")

            return render_template("farmer/market_prices.html", result=res, form_data=data)

        except Exception as e:
            return self.handle_exception(e, "Error calculating grain storage trade-off")
