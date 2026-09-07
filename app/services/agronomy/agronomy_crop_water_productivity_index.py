"""
Agronomy Crop Water Productivity Index Engine for Smart Farmer Assistant.

Quantifies crop water productivity (CWP in kg/m3), yield response to water deficits, and irrigation productivity.
"""

from typing import Dict, Any


class AgronomyCropWaterProductivityEngine:
    """Calculates crop water productivity index and water use efficiency (WUE)."""

    @staticmethod
    def calculate_cwp_and_wue(
        total_yield_kg_per_acre: float,
        total_water_applied_m3_per_acre: float,
        effective_rainfall_m3_per_acre: float = 0.0,
        market_price_per_kg_inr: float = 22.50
    ) -> Dict[str, Any]:
        """
        CWP = Total Yield (kg) / Total Water Consumed (m3)
        Economic Water Productivity (EWP) = (Yield * Price) / Water Consumed (INR/m3)
        """
        gross_water_m3 = max(1.0, total_water_applied_m3_per_acre + effective_rainfall_m3_per_acre)
        cwp_kg_m3 = round(total_yield_kg_per_acre / gross_water_m3, 3)

        gross_revenue_inr = total_yield_kg_per_acre * market_price_per_kg_inr
        ewp_inr_m3 = round(gross_revenue_inr / gross_water_m3, 2)

        return {
            "total_yield_kg_per_acre": total_yield_kg_per_acre,
            "total_water_applied_m3": total_water_applied_m3_per_acre,
            "effective_rainfall_m3": effective_rainfall_m3_per_acre,
            "gross_water_consumed_m3": gross_water_m3,
            "crop_water_productivity_kg_m3": cwp_kg_m3,
            "economic_water_productivity_inr_m3": ewp_inr_m3,
            "water_efficiency_benchmark": "High Efficiency" if cwp_kg_m3 >= 1.2 else ("Moderate Efficiency" if cwp_kg_m3 >= 0.7 else "Low Efficiency")
        }
