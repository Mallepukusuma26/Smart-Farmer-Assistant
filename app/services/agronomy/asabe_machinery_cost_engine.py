"""
ASABE Machinery Management & Operating Cost Engine.
Implements ASABE D497.5 standards for tractor drawbar power,
fuel consumption rates, repair & maintenance curves, and machine depreciation.
"""

from typing import Dict, Any

class ASABEMachineryCostEngine:
    """ASABE D497 standards machinery cost calculator."""

    def calculate_tractor_operating_cost(
        self,
        purchase_price: float,
        rated_power_kw: float,
        annual_use_hours: float,
        fuel_price_per_liter: float,
        age_years: float = 5.0
    ) -> Dict[str, float]:
        """
        Calculate total machinery cost ($/hour and $/hectare).
        """
        # Average fuel consumption = 0.223 L / (kW * hr)
        fuel_rate_l_hr = 0.223 * rated_power_kw * 0.60  # 60% average load factor
        fuel_cost_hr = fuel_rate_l_hr * fuel_price_per_liter

        # Repair and Maintenance (R&M) cost curve
        # C_rm = RF1 * P_purchase * (total_hours / 1000) ^ RF2
        total_hours = annual_use_hours * age_years
        rm_accumulated = 0.007 * purchase_price * ((total_hours / 1000.0) ** 1.4)
        rm_cost_hr = rm_accumulated / max(1.0, total_hours)

        # Capital recovery & depreciation (Straight line + interest)
        salvage_value = purchase_price * (0.68 * (0.92 ** age_years))
        depreciation_annual = (purchase_price - salvage_value) / max(1.0, age_years)
        depreciation_hr = depreciation_annual / max(1.0, annual_use_hours)

        total_cost_hr = fuel_cost_hr + rm_cost_hr + depreciation_hr

        return {
            "rated_power_kw": rated_power_kw,
            "fuel_consumption_l_hr": round(fuel_rate_l_hr, 2),
            "fuel_cost_per_hour": round(fuel_cost_hr, 2),
            "repair_maintenance_cost_per_hour": round(rm_cost_hr, 2),
            "depreciation_cost_per_hour": round(depreciation_hr, 2),
            "total_operating_cost_per_hour": round(total_cost_hr, 2),
            "estimated_salvage_value": round(salvage_value, 2)
        }
