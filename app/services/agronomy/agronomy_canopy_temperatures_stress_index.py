"""
Agronomy Canopy Temperature Stress Index (CWSI) Engine for Smart Farmer Assistant.

Computes Crop Water Stress Index based on canopy and ambient air temperature difference.
"""
from typing import Dict, Any

class AgronomyCanopyTemperatureStressIndexEngine:
    @staticmethod
    def calculate_cwsi(tc_minus_ta: float, lower_baseline: float = -2.5, upper_baseline: float = 4.5) -> Dict[str, Any]:
        cwsi = (tc_minus_ta - lower_baseline) / max(0.1, (upper_baseline - lower_baseline))
        cwsi = min(1.0, max(0.0, round(cwsi, 2)))
        return {
            'canopy_air_temp_diff_c': tc_minus_ta,
            'cwsi': cwsi,
            'irrigation_urgency': 'Immediate Irrigation Required' if cwsi > 0.6 else 'Moderate Stress' if cwsi > 0.3 else 'Well Watered'
        }
