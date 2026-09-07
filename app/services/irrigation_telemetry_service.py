"""
Irrigation Telemetry Service Module for Smart Farmer Assistant.

Calculates reference evapotranspiration (ET0) using the FAO Penman-Monteith equation,
crop evapotranspiration (ETc), soil moisture balance equations, irrigation pump runtime,
and electricity/diesel pumping expense estimation.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class IrrigationTelemetryService:
    """
    Business service executing FAO Penman-Monteith ET0 evapotranspiration math,
    crop stage factor Kc lookup, soil water deficit calculation, and pump operating cost estimation.
    """

    @staticmethod
    def calculate_fao_penman_monteith_et0(
        temperature_c: float,
        relative_humidity_pct: float,
        wind_speed_m_s: float = 2.0,
        solar_radiation_mj_m2: float = 18.0,
        altitude_m: float = 100.0
    ) -> float:
        """
        Calculates reference evapotranspiration (ET0 in mm/day) using FAO Penman-Monteith equation.
        """
        # Atmospheric pressure (kPa)
        p_atm = 101.3 * math.pow((293.0 - 0.0065 * altitude_m) / 293.0, 5.26)

        # Psychrometric constant gamma (kPa/°C)
        gamma = 0.000665 * p_atm

        # Saturation vapor pressure es (kPa)
        es = 0.6108 * math.exp((17.27 * temperature_c) / (temperature_c + 237.3))

        # Actual vapor pressure ea (kPa)
        ea = es * (relative_humidity_pct / 100.0)

        # Slope of saturation vapor pressure curve delta (kPa/°C)
        delta = (4098.0 * es) / math.pow(temperature_c + 237.3, 2)

        # Net radiation Rn (approximate conversion)
        rn = solar_radiation_mj_m2 * 0.408

        # Soil heat flux density G (assumed 0 for daily step)
        g = 0.0

        # FAO Penman-Monteith Equation numerator and denominator
        num = 0.408 * delta * (rn - g) + gamma * (900.0 / (temperature_c + 273.0)) * wind_speed_m_s * (es - ea)
        den = delta + gamma * (1.0 + 0.34 * wind_speed_m_s)

        et0 = num / den if den > 0 else 3.5
        return round(max(et0, 1.0), 2)

    @staticmethod
    def get_crop_coefficient_kc(crop_name: str, growth_stage: str = "mid") -> float:
        """
        Returns crop coefficient Kc for crop type and growth stage (initial, mid, late).
        """
        crop_lower = crop_name.lower().strip()
        kc_table = {
            "rice": {"initial": 1.05, "mid": 1.20, "late": 0.90},
            "wheat": {"initial": 0.40, "mid": 1.15, "late": 0.40},
            "maize": {"initial": 0.30, "mid": 1.20, "late": 0.60},
            "corn": {"initial": 0.30, "mid": 1.20, "late": 0.60},
            "tomato": {"initial": 0.60, "mid": 1.15, "late": 0.80},
            "potato": {"initial": 0.50, "mid": 1.15, "late": 0.75},
            "cotton": {"initial": 0.35, "mid": 1.20, "late": 0.70},
            "soybean": {"initial": 0.40, "mid": 1.15, "late": 0.50},
            "groundnut": {"initial": 0.40, "mid": 1.15, "late": 0.60},
            "sugarcane": {"initial": 0.40, "mid": 1.25, "late": 0.75}
        }
        stage = growth_stage.lower().strip()
        if stage not in ["initial", "mid", "late"]:
            stage = "mid"

        crop_kc = kc_table.get(crop_lower, {"initial": 0.50, "mid": 1.00, "late": 0.60})
        return crop_kc.get(stage, 1.00)

    def calculate_irrigation_requirement(
        self,
        crop_name: str,
        growth_stage: str,
        area_acres: float,
        temperature_c: float,
        relative_humidity_pct: float,
        current_soil_moisture_pct: float,
        target_soil_moisture_pct: float = 80.0
    ) -> Dict[str, Any]:
        """
        Calculates daily crop water requirement (ETc = ET0 * Kc), net water deficit,
        total liters required, pump duration, and estimated electricity cost.
        """
        et0 = self.calculate_fao_penman_monteith_et0(temperature_c, relative_humidity_pct)
        kc = self.get_crop_coefficient_kc(crop_name, growth_stage)
        etc_mm_day = round(et0 * kc, 2)

        # Soil moisture deficit calculation
        moisture_deficit_pct = max(target_soil_moisture_pct - current_soil_moisture_pct, 0.0)
        net_water_depth_mm = round((moisture_deficit_pct / 100.0) * etc_mm_day * 3.0, 2)

        # 1 mm over 1 acre = 4,046.86 Liters
        total_liters = round(net_water_depth_mm * 4046.86 * area_acres, 2)

        # Standard 5 HP Submersible Pump delivers ~250 Liters/Minute (15,000 L/hr)
        pump_flow_rate_lph = 15000.0
        pump_hours_required = round(total_liters / pump_flow_rate_lph, 2) if total_liters > 0 else 0.0

        # Electricity cost: 5 HP = 3.73 kW -> kWh * $0.12/kWh
        energy_kwh = pump_hours_required * 3.73
        pumping_cost_usd = round(energy_kwh * 0.12, 2)

        return {
            "crop_name": crop_name,
            "growth_stage": growth_stage,
            "reference_et0_mm_day": et0,
            "crop_kc": kc,
            "crop_etc_mm_day": etc_mm_day,
            "current_soil_moisture_pct": current_soil_moisture_pct,
            "moisture_deficit_pct": moisture_deficit_pct,
            "net_water_depth_mm": net_water_depth_mm,
            "total_water_required_liters": total_liters,
            "total_water_cubic_meters": round(total_liters / 1000.0, 2),
            "pump_hours_required": pump_hours_required,
            "estimated_pumping_cost_usd": pumping_cost_usd
        }
