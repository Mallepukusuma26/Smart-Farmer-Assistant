"""
Farm Machinery Cost Service Module for Smart Farmer Assistant.

Calculates tractor fuel consumption rate (Liters/Hour), effective field capacity (Acres/Hour),
field efficiency %, repair and maintenance (R&M) cost per hour, and total custom hire rate.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class FarmMachineryCostService:
    """
    Business service calculating machinery operating economics, effective field capacity (EFC),
    ASABE standard fuel consumption, and total cost per acre.
    """

    @staticmethod
    def calculate_effective_field_capacity(
        implement_width_meters: float,
        travel_speed_kmh: float,
        field_efficiency_pct: float = 80.0
    ) -> Dict[str, Any]:
        """
        Calculates Effective Field Capacity (EFC in Acres/Hour and Hectares/Hour):
        EFC (ha/hr) = Width (m) * Speed (km/h) * Efficiency / 10
        """
        width_m = max(implement_width_meters, 0.5)
        speed = max(travel_speed_kmh, 1.0)
        eff = min(max(field_efficiency_pct / 100.0, 0.4), 0.95)

        efc_ha_hr = (width_m * speed * eff) / 10.0
        efc_acres_hr = efc_ha_hr * 2.47105

        time_per_acre_hours = 1.0 / efc_acres_hr if efc_acres_hr > 0 else 0.0

        return {
            "implement_width_meters": width_m,
            "travel_speed_kmh": speed,
            "field_efficiency_pct": field_efficiency_pct,
            "efc_hectares_per_hour": round(efc_ha_hr, 2),
            "efc_acres_per_hour": round(efc_acres_hr, 2),
            "operating_hours_per_acre": round(time_per_acre_hours, 2)
        }

    @staticmethod
    def calculate_tractor_fuel_consumption(
        engine_horsepower_hp: float,
        load_factor_pct: float = 60.0,
        diesel_price_per_liter: float = 1.20
    ) -> Dict[str, Any]:
        """
        Calculates ASABE standard diesel fuel consumption rate:
        Fuel Rate (L/hr) = 0.223 * HP * (Load / 100)
        """
        hp = max(engine_horsepower_hp, 10.0)
        load = min(max(load_factor_pct / 100.0, 0.2), 0.9)

        fuel_lph = 0.223 * hp * load
        fuel_cost_per_hour = fuel_lph * diesel_price_per_liter

        return {
            "engine_horsepower_hp": hp,
            "load_factor_pct": load_factor_pct,
            "diesel_fuel_lph": round(fuel_lph, 2),
            "fuel_cost_per_hour_usd": round(fuel_cost_per_hour, 2),
            "diesel_price_per_liter_usd": diesel_price_per_liter
        }
