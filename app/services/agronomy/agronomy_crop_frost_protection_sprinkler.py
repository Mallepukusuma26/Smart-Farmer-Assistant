"""
Agronomy Crop Frost Protection Sprinkler Engine for Smart Farmer Assistant.

Models latent heat release from overhead sprinkler water application during radiation frost events.
"""

from typing import Dict, Any


class AgronomyCropFrostProtectionEngine:
    """Calculates overhead sprinkler application rate (mm/hr) to protect crops against frost freezing down to -6°C."""

    @staticmethod
    def calculate_sprinkler_frost_protection(
        min_air_temp_c: float,
        wind_speed_km_h: float = 3.0,
        area_acres: float = 1.0
    ) -> Dict[str, Any]:
        """
        Latent heat of fusion = 334 J/g (80 cal/g).
        Required water application rate (mm/hr) increases as temperature drops and wind speed increases.
        """
        frost_deficit_c = max(0.0, 0.0 - min_air_temp_c)
        if frost_deficit_c <= 0:
            return {"status": "No frost protection required — temperature remains above 0°C."}

        base_rate_mm_hr = frost_deficit_c * 0.8
        wind_factor = 1.0 + (wind_speed_km_h / 15.0)
        required_application_rate_mm_hr = round(base_rate_mm_hr * wind_factor, 2)

        # Application volume in m3/hr per acre (1 mm over 1 acre = 4.04686 m3)
        water_flow_m3_hr = round(required_application_rate_mm_hr * 4.04686 * area_acres, 1)

        return {
            "min_forecasted_temp_c": min_air_temp_c,
            "wind_speed_km_h": wind_speed_km_h,
            "required_sprinkler_rate_mm_hr": required_application_rate_mm_hr,
            "total_water_flow_m3_hr": water_flow_m3_hr,
            "latent_heat_protection_c": round(frost_deficit_c, 1),
            "operational_rule": "Turn sprinklers ON when wet-bulb temperature reaches +0.5°C and maintain continuous operation until ice melts after sunrise."
        }
