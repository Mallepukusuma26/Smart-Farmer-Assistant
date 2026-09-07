"""
Agronomy Grain Aeration & Cooling Time Engine for Smart Farmer Assistant.

Models silo aeration fan airflow rates (m3/hr/ton), cooling front velocity, and spoilage prevention.
"""

from typing import Dict, Any


class AgronomyGrainAerationCoolingEngine:
    """Calculates grain bulk aeration fan run-time and cooling front progression in storage silos."""

    @staticmethod
    def calculate_aeration_cooling_time(
        grain_tonnage: float,
        airflow_rate_m3_hr_ton: float = 6.0,
        grain_temp_initial_c: float = 32.0,
        ambient_air_temp_c: float = 18.0,
        fan_power_kw: float = 7.5
    ) -> Dict[str, Any]:
        """Calculates total fan hours required to move cooling front through silo depth."""
        temp_drop_c = max(0.0, grain_temp_initial_c - ambient_air_temp_c)
        if temp_drop_c <= 0:
            return {"status": "No cooling possible — ambient air is warmer than grain bulk."}

        total_airflow_m3_hr = grain_tonnage * airflow_rate_m3_hr_ton
        # Typical specific heat of cereal grain = 1.6 - 2.0 kJ/kg/C
        cooling_hours = round((grain_tonnage * 1000.0 * 1.8 * temp_drop_c) / (total_airflow_m3_hr * 1.2 * 1.005), 1)
        energy_kwh = round(cooling_hours * fan_power_kw, 1)

        return {
            "grain_tonnage": grain_tonnage,
            "airflow_rate_m3_hr_ton": airflow_rate_m3_hr_ton,
            "total_airflow_capacity_m3_hr": round(total_airflow_m3_hr, 1),
            "initial_grain_temp_c": grain_temp_initial_c,
            "target_grain_temp_c": ambient_air_temp_c,
            "required_aeration_hours": cooling_hours,
            "fan_energy_kwh": energy_kwh,
            "estimated_electricity_cost_inr": round(energy_kwh * 7.50, 2),
            "aeration_strategy": "Operate fans during cool night hours (22:00-06:00) when ambient relative humidity is below 70%."
        }
