"""
Crop Insurance Risk Service Module for Smart Farmer Assistant.

Calculates Weather-Index Crop Insurance yield loss indemnity, drought trigger thresholds,
area-yield index coverage, and premium subsidy calculations.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class CropInsuranceRiskService:
    """
    Business service calculating weather-index crop insurance triggers,
    yield loss shortfall indemnity, and net premium payable after government subsidies.
    """

    @staticmethod
    def calculate_yield_index_indemnity(
        guaranteed_yield_tonnes_acre: float,
        actual_harvested_yield_tonnes_acre: float,
        sum_insured_usd_acre: float,
        subsidy_pct: float = 50.0
    ) -> Dict[str, Any]:
        """
        Calculates Area-Yield Crop Insurance Loss Indemnity:
        Indemnity = [(Guaranteed Yield - Actual Yield) / Guaranteed Yield] * Sum Insured
        """
        if actual_harvested_yield_tonnes_acre >= guaranteed_yield_tonnes_acre:
            return {
                "guaranteed_yield_tonnes_acre": guaranteed_yield_tonnes_acre,
                "actual_harvested_yield_tonnes_acre": actual_harvested_yield_tonnes_acre,
                "yield_shortfall_pct": 0.0,
                "indemnity_payout_usd_acre": 0.0,
                "status": "Harvest Exceeds Target — No Indemnity Payable"
            }

        shortfall = guaranteed_yield_tonnes_acre - actual_harvested_yield_tonnes_acre
        shortfall_pct = (shortfall / guaranteed_yield_tonnes_acre) * 100.0

        indemnity_per_acre = (shortfall / guaranteed_yield_tonnes_acre) * sum_insured_usd_acre

        # Standard premium rate (e.g. 5% of Sum Insured)
        gross_premium = sum_insured_usd_acre * 0.05
        net_farmer_premium = gross_premium * (1.0 - (subsidy_pct / 100.0))

        return {
            "guaranteed_yield_tonnes_acre": guaranteed_yield_tonnes_acre,
            "actual_harvested_yield_tonnes_acre": actual_harvested_yield_tonnes_acre,
            "yield_shortfall_tonnes_acre": round(shortfall, 2),
            "yield_shortfall_pct": round(shortfall_pct, 2),
            "sum_insured_usd_acre": sum_insured_usd_acre,
            "gross_premium_usd_acre": round(gross_premium, 2),
            "government_subsidy_pct": subsidy_pct,
            "net_farmer_premium_usd_acre": round(net_farmer_premium, 2),
            "indemnity_payout_usd_acre": round(indemnity_per_acre, 2),
            "net_insurance_benefit_usd_acre": round(indemnity_per_acre - net_farmer_premium, 2)
        }
