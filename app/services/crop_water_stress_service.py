"""
Crop Water Stress Service Module for Smart Farmer Assistant.

Calculates Crop Water Stress Index (CWSI), canopy-to-air temperature delta (Tc - Ta),
vapor pressure deficit (VPD), and thermal stress thresholds.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class CropWaterStressService:
    """
    Business service calculating Crop Water Stress Index (CWSI) from infrared canopy temperature,
    ambient air temperature, and air vapor pressure deficit (VPD).
    """

    @staticmethod
    def calculate_cwsi(
        canopy_temp_c: float,
        air_temp_c: float,
        vpd_kpa: float = 1.5,
        lower_baseline_slope: float = -1.8,
        lower_baseline_intercept: float = 1.5
    ) -> Dict[str, Any]:
        """
        Calculates Crop Water Stress Index (CWSI) bounded between 0.0 (Well-Watered) and 1.0 (Severe Stress):
        CWSI = [(Tc - Ta) - (Tc - Ta)_lower] / [(Tc - Ta)_upper - (Tc - Ta)_lower]
        """
        dt_actual = canopy_temp_c - air_temp_c

        # Non-water-stressed baseline (lower limit)
        dt_lower = lower_baseline_slope * vpd_kpa + lower_baseline_intercept

        # Fully stressed non-transpiring baseline (upper limit)
        dt_upper = 5.0

        if dt_upper <= dt_lower:
            cwsi = 0.5
        else:
            cwsi = (dt_actual - dt_lower) / (dt_upper - dt_lower)

        cwsi = round(max(min(cwsi, 1.0), 0.0), 2)

        if cwsi <= 0.2:
            status = "Well-Watered — No Water Stress"
            action = "Irrigation not needed today."
        elif cwsi <= 0.5:
            status = "Mild Water Stress"
            action = "Schedule irrigation within next 48 hours."
        elif cwsi <= 0.8:
            status = "Moderate Water Stress"
            action = "Initiate field irrigation immediately."
        else:
            status = "Severe Water Stress — Stomatal Closure & Yield Loss"
            action = "Apply emergency irrigation to prevent irreversible crop damage."

        return {
            "canopy_temp_c": canopy_temp_c,
            "air_temp_c": air_temp_c,
            "delta_temp_c": round(dt_actual, 2),
            "vpd_kpa": vpd_kpa,
            "cwsi_score": cwsi,
            "water_stress_status": status,
            "recommended_action": action
        }
