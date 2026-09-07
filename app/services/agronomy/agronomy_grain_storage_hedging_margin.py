"""
Agronomy Grain Storage Hedging Margin Engine for Smart Farmer Assistant.

Models grain warehouse storage carry costs, futures basis, and optimal post-harvest sale month.
"""

from typing import Dict, Any, List


class AgronomyGrainStorageHedgingEngine:
    """Calculates grain storage carry cost (storage fee + interest + shrinkage) vs expected seasonal market price appreciation."""

    @staticmethod
    def calculate_storage_carry_margin(
        harvest_price_per_quintal_inr: float,
        monthly_storage_fee_inr: float = 15.0,
        monthly_interest_rate_pct: float = 0.8,
        monthly_shrinkage_pct: float = 0.3,
        storage_months: int = 4
    ) -> Dict[str, Any]:
        """Calculates breakeven future sale price per quintal after N months of storage."""
        total_carry_cost = 0.0
        current_cost_base = harvest_price_per_quintal_inr

        for m in range(1, storage_months + 1):
            interest = current_cost_base * (monthly_interest_rate_pct / 100.0)
            shrinkage = current_cost_base * (monthly_shrinkage_pct / 100.0)
            carry_m = monthly_storage_fee_inr + interest + shrinkage
            total_carry_cost += carry_m
            current_cost_base += carry_m

        breakeven_sale_price = round(harvest_price_per_quintal_inr + total_carry_cost, 2)
        target_price_15pct = round(breakeven_sale_price * 1.15, 2)

        return {
            "harvest_spot_price_inr": harvest_price_per_quintal_inr,
            "planned_storage_duration_months": storage_months,
            "total_carry_cost_per_quintal_inr": round(total_carry_cost, 2),
            "breakeven_sale_price_inr": breakeven_sale_price,
            "target_mandi_sale_price_15pct_margin_inr": target_price_15pct,
            "market_recommendation": f"Hold grain only if expected mandi market price in month {storage_months} exceeds ₹{breakeven_sale_price}/quintal."
        }
