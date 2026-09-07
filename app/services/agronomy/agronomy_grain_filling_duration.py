"""
Agronomy Grain Filling Duration Model for Smart Farmer Assistant.

Estimates grain filling phase duration based on thermal time, temperature stress, and soil moisture.
"""
from typing import Dict, Any

class AgronomyGrainFillingDurationEngine:
    @staticmethod
    def calculate_grain_filling_period(base_temp_c: float, max_temp_c: float, gdd_required: float, avg_daily_temp: float, moisture_stress_factor: float = 1.0) -> Dict[str, Any]:
        daily_gdd = max(0.0, avg_daily_temp - base_temp_c)
        if max_temp_c > 35.0:
            daily_gdd *= 0.85
        daily_gdd *= max(0.5, min(1.0, moisture_stress_factor))
        if daily_gdd <= 0:
            estimated_days = 999.0
        else:
            estimated_days = round(gdd_required / daily_gdd, 1)
        return {
            'daily_gdd': round(daily_gdd, 2),
            'estimated_grain_filling_days': estimated_days,
            'moisture_stress_applied': moisture_stress_factor < 0.8,
            'heat_stress_detected': max_temp_c > 35.0
        }
