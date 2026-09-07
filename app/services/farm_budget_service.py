"""
Farm Budget Service Module for Smart Farmer Assistant.

Manages enterprise budget creation, machinery depreciation math (MACRS / Straight Line),
operating interest calculations, break-even yield/price analysis, and cost per acre breakdown.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class FarmBudgetService:
    """
    Business service providing enterprise budgeting, MACRS asset depreciation,
    operating capital interest calculation, and break-even price matrix.
    """

    @staticmethod
    def calculate_machinery_depreciation(
        purchase_price: float,
        salvage_value: float = 0.0,
        useful_life_years: int = 7,
        method: str = "straight_line"
    ) -> Dict[str, Any]:
        """
        Calculates annual asset depreciation for tractor, harvester, or irrigation pump.
        """
        if method == "macrs_7yr":
            # 7-year MACRS schedule percentages
            macrs_rates = [0.1429, 0.2449, 0.1749, 0.1249, 0.0893, 0.0892, 0.0893, 0.0446]
            annual_depr = [round(purchase_price * r, 2) for r in macrs_rates]
            return {
                "method": "MACRS 7-Year",
                "purchase_price": purchase_price,
                "annual_depreciation_schedule": annual_depr,
                "year_1_depreciation": annual_depr[0]
            }
        else:
            annual_depr_val = (purchase_price - salvage_value) / useful_life_years if useful_life_years > 0 else 0.0
            return {
                "method": "Straight-Line",
                "purchase_price": purchase_price,
                "salvage_value": salvage_value,
                "useful_life_years": useful_life_years,
                "annual_depreciation_usd": round(annual_depr_val, 2)
            }

    @staticmethod
    def generate_enterprise_budget(
        crop_name: str,
        land_area_acres: float,
        variable_costs: Dict[str, float],
        fixed_costs: Dict[str, float],
        expected_yield_per_acre: float,
        expected_price_per_unit: float
    ) -> Dict[str, Any]:
        """
        Generates detailed enterprise budget breakdown, gross margin, return above variable costs,
        and break-even yield and price matrix.
        """
        total_variable = sum(variable_costs.values()) * land_area_acres
        total_fixed = sum(fixed_costs.values()) * land_area_acres
        total_cost = total_variable + total_fixed

        total_production = expected_yield_per_acre * land_area_acres
        gross_revenue = total_production * expected_price_per_unit

        return_above_variable = gross_revenue - total_variable
        net_profit = gross_revenue - total_cost

        # Break-even calculations
        be_yield_var = (total_variable / land_area_acres) / expected_price_per_unit if expected_price_per_unit > 0 else 0.0
        be_yield_total = (total_cost / land_area_acres) / expected_price_per_unit if expected_price_per_unit > 0 else 0.0

        be_price_var = (total_variable / land_area_acres) / expected_yield_per_acre if expected_yield_per_acre > 0 else 0.0
        be_price_total = (total_cost / land_area_acres) / expected_yield_per_acre if expected_yield_per_acre > 0 else 0.0

        return {
            "crop_name": crop_name,
            "land_area_acres": land_area_acres,
            "gross_revenue_usd": round(gross_revenue, 2),
            "total_variable_costs_usd": round(total_variable, 2),
            "total_fixed_costs_usd": round(total_fixed, 2),
            "total_production_cost_usd": round(total_cost, 2),
            "return_above_variable_costs_usd": round(return_above_variable, 2),
            "net_profit_usd": round(net_profit, 2),
            "cost_per_acre": round(total_cost / land_area_acres, 2) if land_area_acres > 0 else 0.0,
            "break_even_metrics": {
                "break_even_yield_variable_tonnes_acre": round(be_yield_var, 2),
                "break_even_yield_total_tonnes_acre": round(be_yield_total, 2),
                "break_even_price_variable_usd_tonne": round(be_price_var, 2),
                "break_even_price_total_usd_tonne": round(be_price_total, 2)
            }
        }
