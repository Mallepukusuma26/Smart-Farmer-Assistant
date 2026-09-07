"""
Agronomy Crop Heat Unit (CHU) Accumulation Engine for Smart Farmer Assistant.

Models Ontario Crop Heat Units (CHU) for corn and soybean thermal maturity modeling.
"""

from typing import Dict, Any, List


class AgronomyCropHeatUnitEngine:
    """Calculates Crop Heat Units (CHU = (Ymax + Ymin) / 2) based on daily max/min temperatures."""

    @staticmethod
    def calculate_chu_accumulation(
        daily_max_temps_c: List[float],
        daily_min_temps_c: List[float]
    ) -> Dict[str, Any]:
        """
        Ymax = 3.33 * (Tmax - 10) - 0.084 * (Tmax - 10)^2
        Ymin = 1.8 * (Tmin - 4.4)
        """
        total_chu = 0.0
        days = len(daily_max_temps_c)

        for i in range(days):
            tmax = daily_max_temps_c[i]
            tmin = daily_min_temps_c[i]

            ymax = max(0.0, (3.33 * (tmax - 10.0)) - (0.084 * ((tmax - 10.0) ** 2))) if tmax > 10.0 else 0.0
            ymin = max(0.0, 1.8 * (tmin - 4.4)) if tmin > 4.4 else 0.0

            chu_day = (ymax + ymin) / 2.0
            total_chu += chu_day

        total_chu = round(total_chu, 1)

        maturity_eval = "Corn / Maize Fully Mature (> 2800 CHU)" if total_chu >= 2800.0 else (
            "Silking / Dough Stage (2000-2700 CHU)" if total_chu >= 2000.0 else "Vegetative Stage (< 2000 CHU)"
        )

        return {
            "monitored_days_count": days,
            "cumulative_crop_heat_units_chu": total_chu,
            "avg_daily_chu": round(total_chu / max(1, days), 1),
            "maturity_evaluation": maturity_eval
        }
