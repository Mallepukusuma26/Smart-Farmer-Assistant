"""
Agronomy Greenhouse Transpiration & Microclimate Engine for Smart Farmer Assistant.

Models greenhouse crop transpiration rate (g/m2/hr), Vapor Pressure Deficit (VPD), and fogging cooling needs.
"""

import math
from typing import Dict, Any


class AgronomyGreenhouseTranspirationEngine:
    """Calculates greenhouse transpiration rates and microclimate VPD optimization."""

    @staticmethod
    def calculate_transpiration_and_vpd(
        air_temp_c: float,
        relative_humidity_pct: float,
        solar_radiation_w_m2: float = 400.0,
        leaf_area_index: float = 3.0
    ) -> Dict[str, Any]:
        """
        Saturated Vapor Pressure (VP_sat) = 0.61078 * exp((17.27 * T) / (T + 237.3))
        Actual Vapor Pressure (VP_act) = VP_sat * (RH / 100)
        VPD = VP_sat - VP_act (Target VPD: 0.8 - 1.2 kPa)
        """
        vp_sat = 0.61078 * math.exp((17.27 * air_temp_c) / (air_temp_c + 237.3))
        vp_act = vp_sat * (relative_humidity_pct / 100.0)
        vpd_kpa = round(vp_sat - vp_act, 2)

        # Transpiration estimate in g/m2/hr
        transpiration_g_m2_hr = round(max(10.0, (solar_radiation_w_m2 * 0.4) + (vpd_kpa * 80.0 * leaf_area_index)), 1)
        transpiration_liters_m2_day = round((transpiration_g_m2_hr * 12.0) / 1000.0, 2)

        vpd_status = "Optimal Transpiration Zone (0.8 - 1.2 kPa)" if 0.8 <= vpd_kpa <= 1.2 else (
            "High Stress (VPD > 1.2 kPa — Turn on High-Pressure Foggers)" if vpd_kpa > 1.2 else "Low Transpiration / Fungal Risk (VPD < 0.8 kPa — Increase Ventilation)"
        )

        return {
            "air_temperature_c": air_temp_c,
            "relative_humidity_pct": relative_humidity_pct,
            "vapor_pressure_deficit_vpd_kpa": vpd_kpa,
            "vpd_health_status": vpd_status,
            "hourly_transpiration_g_m2_hr": transpiration_g_m2_hr,
            "daily_crop_water_transpired_liters_m2": transpiration_liters_m2_day
        }
