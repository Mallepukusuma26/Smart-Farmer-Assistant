"""
Agronomy Farm Machinery Operating Life Engine for Smart Farmer Assistant.

Models tractor/implement wear and tear, ASABE remaining useful life (RUL), and overhaul scheduling.
"""

from typing import Dict, Any


class AgronomyMachineryOperatingLifeEngine:
    """Calculates tractor and implement cumulative operating hours, wear factor, and salvage value percentage."""

    @staticmethod
    def calculate_machine_remaining_life(
        machine_type: str,
        cumulative_hours_used: float,
        purchase_price_inr: float,
        annual_hours_use: float = 500.0
    ) -> Dict[str, Any]:
        """
        ASABE Estimated Useful Life (Hours):
        - 4WD Tractor: 12,000 hrs
        - Combine Harvester: 3,000 hrs
        - Rotavator / Tillage: 2,500 hrs
        - Seed Drill / Planter: 1,500 hrs
        """
        life_expectancy_map = {
            "4WD Tractor": 12000.0,
            "2WD Tractor": 10000.0,
            "Combine Harvester": 3000.0,
            "Rotavator": 2500.0,
            "Disc Harrow": 2000.0,
            "Seed Drill": 1500.0
        }

        total_expected_hours = life_expectancy_map.get(machine_type, 8000.0)
        remaining_hours = max(0.0, total_expected_hours - cumulative_hours_used)
        used_pct = round(min(100.0, (cumulative_hours_used / total_expected_hours) * 100.0), 1)

        remaining_years = round(remaining_hours / annual_hours_use, 1) if annual_hours_use > 0 else 0.0

        # ASABE Remaining Value % formula: RV = 68 * (0.92 ^ (cumulative_hours / 1000))
        remaining_value_pct = round(max(5.0, 68.0 * (0.92 ** (cumulative_hours_used / 1000.0))), 1)
        estimated_resale_value_inr = round(purchase_price_inr * (remaining_value_pct / 100.0), 2)

        return {
            "machine_type": machine_type,
            "cumulative_hours_used": cumulative_hours_used,
            "total_design_life_hours": total_expected_hours,
            "life_consumed_pct": used_pct,
            "remaining_useful_hours": remaining_hours,
            "estimated_remaining_years": remaining_years,
            "asabe_remaining_value_pct": remaining_value_pct,
            "estimated_current_resale_value_inr": estimated_resale_value_inr,
            "maintenance_action": "OVERHAUL / REPLACEMENT DUE" if used_pct >= 85.0 else "Routine Preventive Maintenance Schedule"
        }
