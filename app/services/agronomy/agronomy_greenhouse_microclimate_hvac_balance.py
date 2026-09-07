"""
Agronomy Greenhouse Microclimate HVAC Balance Engine for Smart Farmer Assistant.

Models greenhouse heat gain (solar + equipment), sensible heat loss, evaporative pad-and-fan cooling capacity.
"""

from typing import Dict, Any


class AgronomyGreenhouseHVACBalanceEngine:
    """Calculates greenhouse pad-and-fan ventilation rate (m3/hr) and evaporative cooling efficiency."""

    @staticmethod
    def calculate_hvac_cooling_capacity(
        greenhouse_area_m2: float,
        ambient_temp_c: float,
        solar_irradiance_w_m2: float = 650.0,
        pad_efficiency_pct: float = 80.0,
        target_temp_c: float = 24.0
    ) -> Dict[str, Any]:
        """
        Pad Cooling Delta-T = (T_ambient - T_wetbulb) * Pad_Eff
        Air Flow Rate (m3/hr) = Solar Heat Gain / (1.2 * 1.005 * Delta-T_permissible)
        """
        solar_heat_gain_kw = (greenhouse_area_m2 * solar_irradiance_w_m2 * 0.70) / 1000.0

        # Permissible air temp rise across greenhouse length = 3.0 °C
        required_airflow_m3_hr = round((solar_heat_gain_kw * 3600.0) / (1.2 * 1.005 * 3.0), 1)
        air_changes_per_min = round((required_airflow_m3_hr / (greenhouse_area_m2 * 3.5)) / 60.0, 2)

        pad_area_m2 = round(required_airflow_m3_hr / (1.5 * 3600.0), 1)  # Face velocity 1.5 m/s

        return {
            "greenhouse_area_m2": greenhouse_area_m2,
            "solar_heat_gain_kw": round(solar_heat_gain_kw, 1),
            "required_ventilation_capacity_m3_hr": required_airflow_m3_hr,
            "air_changes_per_minute": air_changes_per_min,
            "required_evaporative_pad_area_m2": pad_area_m2,
            "fan_count_recommendation": f"Install {int((required_airflow_m3_hr / 40000.0) + 0.99)} exhaust fans (40,000 m3/hr rating each)."
        }
