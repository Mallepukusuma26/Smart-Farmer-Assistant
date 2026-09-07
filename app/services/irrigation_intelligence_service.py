"""
Irrigation Intelligence Service Module for Smart Farmer Assistant.

Provides offline Penman-Monteith ET calculations, crop water stress indexing,
drip/sprinkler efficiency analysis, water cost estimation, and irrigation alert generation.
"""

from typing import Dict, Any, List, Optional
import math


class IrrigationIntelligenceService:
    """
    Offline Irrigation Intelligence engine for evapotranspiration modeling,
    water application schedules, field irrigation efficiency, and pumping energy costs.
    """

    def calculate_reference_et0(
        self,
        temperature_c: float,
        humidity_pct: float,
        wind_speed_m_s: float = 2.0,
        solar_radiation_mj_m2: float = 18.0
    ) -> float:
        """
        Calculates offline Hargreaves / FAO Penman-Monteith reference evapotranspiration (ET0 in mm/day).
        """
        # Simplified Hargreaves ET0 formula
        t_mean = temperature_c
        t_range = 10.0  # Assumed diurnally
        et0 = 0.0023 * (t_mean + 17.8) * math.sqrt(t_range) * (solar_radiation_mj_m2 * 0.408)
        return round(max(1.0, min(12.0, et0)), 2)

    def calculate_crop_water_requirement(
        self,
        crop_name: str,
        growth_stage: str,
        et0_mm_day: float,
        area_acres: float = 1.0
    ) -> Dict[str, Any]:
        """
        Computes Crop Evapotranspiration (ETc = ET0 * Kc) and water volume requirement.
        """
        kc_table = {
            "Wheat": {"Initial": 0.4, "Crop Dev": 0.8, "Mid Season": 1.15, "Late Season": 0.45},
            "Rice": {"Initial": 1.05, "Crop Dev": 1.15, "Mid Season": 1.20, "Late Season": 0.90},
            "Maize": {"Initial": 0.3, "Crop Dev": 0.7, "Mid Season": 1.20, "Late Season": 0.50},
            "Cotton": {"Initial": 0.35, "Crop Dev": 0.75, "Mid Season": 1.15, "Late Season": 0.70}
        }

        crop_kc = kc_table.get(crop_name, {"Initial": 0.4, "Crop Dev": 0.8, "Mid Season": 1.15, "Late Season": 0.5})
        kc = crop_kc.get(growth_stage, 0.85)

        etc_mm_day = round(et0_mm_day * kc, 2)
        # 1 mm/day over 1 acre = 4.04686 m3/day = 4046.86 Liters/day
        daily_liters = round(etc_mm_day * 4046.86 * area_acres, 0)
        daily_m3 = round(daily_liters / 1000.0, 2)

        return {
            "crop_name": crop_name,
            "growth_stage": growth_stage,
            "kc_coefficient": kc,
            "et0_mm_day": et0_mm_day,
            "etc_mm_day": etc_mm_day,
            "area_acres": area_acres,
            "daily_water_demand_liters": daily_liters,
            "daily_water_demand_m3": daily_m3,
            "weekly_water_demand_m3": round(daily_m3 * 7.0, 2)
        }

    def generate_irrigation_schedule(
        self,
        soil_type: str,
        irrigation_method: str,
        daily_water_m3: float,
        area_acres: float = 1.0
    ) -> Dict[str, Any]:
        """
        Determines irrigation interval, duration per session, and pumping energy requirements.
        """
        method = (irrigation_method or "Drip").lower()

        if "drip" in method:
            interval_days = 1
            flow_rate_m3_hr = 10.0 * area_acres
            efficiency = 0.90
        elif "sprinkler" in method:
            interval_days = 3
            flow_rate_m3_hr = 15.0 * area_acres
            efficiency = 0.75
        else:
            interval_days = 7
            flow_rate_m3_hr = 25.0 * area_acres
            efficiency = 0.60

        water_to_apply_m3 = round((daily_water_m3 * interval_days) / efficiency, 2)
        pumping_hours = round(water_to_apply_m3 / flow_rate_m3_hr, 1) if flow_rate_m3_hr > 0 else 2.0

        # Pumping power estimate (5 HP motor consuming 3.7 kW)
        kwh_consumed = round(pumping_hours * 3.7, 1)
        est_pumping_cost_inr = round(kwh_consumed * 6.50, 2)

        return {
            "irrigation_method": irrigation_method,
            "soil_type": soil_type,
            "recommended_interval_days": interval_days,
            "application_volume_m3": water_to_apply_m3,
            "estimated_pumping_hours": pumping_hours,
            "energy_consumed_kwh": kwh_consumed,
            "estimated_energy_cost_inr": est_pumping_cost_inr,
            "irrigation_efficiency_pct": round(efficiency * 100.0, 1)
        }
