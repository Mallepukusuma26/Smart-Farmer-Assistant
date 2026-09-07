"""
Crop Water Stress Index (CWSI) Thermal Engine.
Calculates canopy temperature depression (Tc - Ta) and CWSI ratio using
non-water-stressed lower baseline and fully stressed upper baseline equations.
"""

import math
from typing import Dict, Any

class CropWaterStressIndexEngine:
    """Canopy temperature water stress index calculator."""

    def calculate_cwsi(
        self,
        canopy_temp_c: float,
        air_temp_c: float,
        relative_humidity_pct: float,
        baseline_a: float = 1.8,
        baseline_b: float = -1.4
    ) -> Dict[str, float]:
        """
        CWSI = [(Tc - Ta) - (Tc - Ta)_lower] / [(Tc - Ta)_upper - (Tc - Ta)_lower]
        """
        # Saturation vapor pressure deficit (VPD) in kPa
        vp_sat = 0.61078 * math.exp((17.27 * air_temp_c) / (air_temp_c + 237.3))
        vpd_kpa = vp_sat * (1.0 - relative_humidity_pct / 100.0)

        dT_actual = canopy_temp_c - air_temp_c
        dT_lower = baseline_a + baseline_b * vpd_kpa  # Non-water-stressed baseline
        dT_upper = baseline_a + baseline_b * 0.0 + 3.5  # Fully-stressed baseline (zero transpiration)

        cwsi = (dT_actual - dT_lower) / max(0.1, (dT_upper - dT_lower))
        cwsi = round(max(0.0, min(1.0, cwsi)), 2)

        if cwsi < 0.2:
            status = "Well Watered (No Stress)"
            recommendation = "No immediate irrigation required."
        elif cwsi < 0.5:
            status = "Mild Water Stress"
            recommendation = "Schedule irrigation within 2-3 days."
        elif cwsi < 0.8:
            status = "Moderate to High Stress"
            recommendation = "Apply irrigation immediately to prevent yield loss."
        else:
            status = "Severe Drought Stress"
            recommendation = "Critical irrigation deficit — crop damage occurring."

        return {
            "canopy_temp_c": canopy_temp_c,
            "air_temp_c": air_temp_c,
            "temp_difference_c": round(dT_actual, 2),
            "vpd_kpa": round(vpd_kpa, 2),
            "cwsi_ratio": cwsi,
            "stress_status": status,
            "irrigation_recommendation": recommendation
        }
