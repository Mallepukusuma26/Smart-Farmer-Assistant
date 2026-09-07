"""
Crop Market Analytics Service Module for Smart Farmer Assistant.

Manages commodity price volatility indexing, storage cost vs selling delay trade-offs,
regional market mandi price comparisons, and optimal harvest timing analytics.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class CropMarketAnalyticsService:
    """
    Business service analyzing market price volatility, storage cost economics,
    price momentum, and optimal harvest selling windows.
    """

    @staticmethod
    def calculate_storage_tradeoff(
        current_price_per_tonne: float,
        expected_future_price_per_tonne: float,
        quantity_tonnes: float,
        storage_cost_per_tonne_month: float = 5.0,
        holding_months: int = 3,
        interest_rate_annual_pct: float = 6.0
    ) -> Dict[str, Any]:
        """
        Calculates net economic gain/loss of storing harvested grain vs selling immediately.
        """
        immediate_revenue = current_price_per_tonne * quantity_tonnes
        future_gross_revenue = expected_future_price_per_tonne * quantity_tonnes

        # Total storage fees
        total_storage_fee = storage_cost_per_tonne_month * quantity_tonnes * holding_months

        # Opportunity cost of capital (interest unearned)
        capital_cost = immediate_revenue * (interest_rate_annual_pct / 100.0) * (holding_months / 12.0)

        total_holding_cost = total_storage_fee + capital_cost
        future_net_revenue = future_gross_revenue - total_holding_cost

        net_economic_benefit = future_net_revenue - immediate_revenue

        return {
            "immediate_revenue_usd": round(immediate_revenue, 2),
            "future_gross_revenue_usd": round(future_gross_revenue, 2),
            "total_storage_fee_usd": round(total_storage_fee, 2),
            "capital_opportunity_cost_usd": round(capital_cost, 2),
            "total_holding_cost_usd": round(total_holding_cost, 2),
            "future_net_revenue_usd": round(future_net_revenue, 2),
            "net_economic_gain_loss_usd": round(net_economic_benefit, 2),
            "recommendation": "Store and Hold for Future Sale" if net_economic_benefit > 0 else "Sell Immediately at Harvest"
        }
