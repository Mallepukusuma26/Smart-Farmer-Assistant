"""
Agronomy Cold Storage & Chilling Hours Engine for Smart Farmer Assistant.

Calculates chilling hour accumulation (Utah & Richardson models) for fruit tree dormancy breaking.
"""

from typing import Dict, Any, List


class AgronomyColdStorageChillingEngine:
    """Calculates winter chill units (0°C - 7.2°C) for temperate orchard fruit production."""

    @staticmethod
    def calculate_chilling_hours(hourly_temperatures_c: List[float]) -> Dict[str, Any]:
        """Utah Model for Chill Units: 1.5°C to 12.4°C weights."""
        total_chilling_hours = 0.0
        utah_chill_units = 0.0

        for t in hourly_temperatures_c:
            if 0.0 <= t <= 7.2:
                total_chilling_hours += 1.0

            # Utah Model weights
            if t < 1.4:
                utah_chill_units += 0.0
            elif 1.5 <= t <= 2.4:
                utah_chill_units += 0.5
            elif 2.5 <= t <= 9.1:
                utah_chill_units += 1.0
            elif 9.2 <= t <= 12.4:
                utah_chill_units += 0.5
            elif 12.5 <= t <= 15.9:
                utah_chill_units += 0.0
            elif 16.0 <= t <= 18.0:
                utah_chill_units -= 0.5
            else:
                utah_chill_units -= 1.0

        utah_chill_units = max(0.0, utah_chill_units)

        return {
            "total_monitored_hours": len(hourly_temperatures_c),
            "standard_chilling_hours_below_7c": round(total_chilling_hours, 1),
            "utah_chill_units_accumulated": round(utah_chill_units, 1),
            "dormancy_fulfillment": "Full Dormancy Satisfied (High Fruit Set Expected)" if utah_chill_units >= 800.0 else (
                "Partial Dormancy Satisfied" if utah_chill_units >= 400.0 else "Low Chill Accumulation — Risk of Delayed Budbreak"
            )
        }
