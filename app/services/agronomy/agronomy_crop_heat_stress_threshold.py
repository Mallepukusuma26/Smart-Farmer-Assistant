"""
Agronomy Crop Heat Stress Threshold Engine for Smart Farmer Assistant.

Models high-temperature canopy heat stress, pollen sterility risk, and thermal cooling requirements.
"""

from typing import Dict, Any


class AgronomyCropHeatStressEngine:
    """Calculates crop heat stress index, pollen sterility risk %, and thermal mitigation advice."""

    @staticmethod
    def calculate_heat_stress_risk(
        crop_name: str,
        max_temperature_c: float,
        relative_humidity_pct: float = 45.0,
        exposure_hours: float = 4.0
    ) -> Dict[str, Any]:
        """Calculates temperature excess over critical threshold during reproductive flowering stage."""
        critical_thresholds = {
            "Wheat": 30.0,
            "Rice": 35.0,
            "Maize": 34.0,
            "Cotton": 38.0,
            "Tomato": 32.0,
            "Potato": 28.0
        }

        threshold_c = critical_thresholds.get(crop_name, 32.0)
        temp_excess = max(0.0, max_temperature_c - threshold_c)

        # Sterility risk % accumulates with exposure duration
        sterility_risk_pct = round(min(100.0, temp_excess * exposure_hours * 6.5), 1)

        heat_stress_category = "Severe Heat Stress" if sterility_risk_pct >= 60.0 else (
            "Moderate Heat Stress" if sterility_risk_pct >= 25.0 else "Minimal Heat Stress"
        )

        return {
            "crop_name": crop_name,
            "max_temperature_c": max_temperature_c,
            "critical_threshold_c": threshold_c,
            "temperature_excess_c": round(temp_excess, 1),
            "exposure_hours": exposure_hours,
            "estimated_pollen_sterility_risk_pct": sterility_risk_pct,
            "heat_stress_category": heat_stress_category,
            "cooling_recommendation": "Apply micro-sprinkler misting or light overhead irrigation during peak thermal hours (12:00-15:00)." if temp_excess > 2.0 else "Temperature is within acceptable growth bounds."
        }
