"""
Market Price Service Module for Smart Farmer Assistant.

Manages local agricultural commodity price tracking, crop price trends,
minimum support price (MSP) references, price forecasting, and market location records.
"""

from typing import Dict, Any, List, Optional
import random
import logging

logger = logging.getLogger(__name__)


class MarketPriceService:
    """
    Business service tracking local crop commodity market prices, regional mandis,
    historical price volatility, and minimum support price references.
    """

    def __init__(self):
        self.reference_prices = {
            "rice": {"price_per_tonne": 450.0, "msp_per_tonne": 420.0, "unit": "USD/Tonne", "trend": "stable"},
            "wheat": {"price_per_tonne": 380.0, "msp_per_tonne": 350.0, "unit": "USD/Tonne", "trend": "upward"},
            "maize": {"price_per_tonne": 310.0, "msp_per_tonne": 290.0, "unit": "USD/Tonne", "trend": "upward"},
            "corn": {"price_per_tonne": 310.0, "msp_per_tonne": 290.0, "unit": "USD/Tonne", "trend": "upward"},
            "tomato": {"price_per_tonne": 650.0, "msp_per_tonne": 500.0, "unit": "USD/Tonne", "trend": "volatile"},
            "potato": {"price_per_tonne": 320.0, "msp_per_tonne": 280.0, "unit": "USD/Tonne", "trend": "stable"},
            "soybean": {"price_per_tonne": 580.0, "msp_per_tonne": 540.0, "unit": "USD/Tonne", "trend": "upward"},
            "groundnut": {"price_per_tonne": 750.0, "msp_per_tonne": 700.0, "unit": "USD/Tonne", "trend": "stable"},
            "cotton": {"price_per_tonne": 1200.0, "msp_per_tonne": 1100.0, "unit": "USD/Tonne", "trend": "downward"},
            "sugarcane": {"price_per_tonne": 45.0, "msp_per_tonne": 40.0, "unit": "USD/Tonne", "trend": "stable"}
        }

    def get_current_market_price(self, crop_name: str) -> Dict[str, Any]:
        """
        Returns local commodity price, minimum support price, and trend status for crop.
        """
        crop_lower = crop_name.lower().strip()
        data = self.reference_prices.get(
            crop_lower,
            {"price_per_tonne": 400.0, "msp_per_tonne": 360.0, "unit": "USD/Tonne", "trend": "stable"}
        )

        return {
            "crop_name": crop_name,
            "market_price_per_tonne": data["price_per_tonne"],
            "msp_per_tonne": data["msp_per_tonne"],
            "unit": data["unit"],
            "price_trend": data["trend"],
            "recommended_selling_window": "Next 14 Days" if data["trend"] == "upward" else "Immediate Sale"
        }

    def get_all_market_prices(self) -> List[Dict[str, Any]]:
        """
        Lists all tracked commodity market price rates.
        """
        service = MarketPriceService()
        result = []
        for crop_name, data in service.reference_prices.items():
            result.append({
                "crop_name": crop_name.capitalize(),
                "price_per_tonne": data["price_per_tonne"],
                "msp_per_tonne": data["msp_per_tonne"],
                "trend": data["trend"]
            })
        return result
