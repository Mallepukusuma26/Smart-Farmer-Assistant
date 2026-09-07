"""
Agronomy Scientific Engines Generator for Smart Farmer Assistant.
Creates production-grade mathematical models and agronomic calculation engines.
"""

import os

AGRONOMY_DIR = os.path.join("app", "services", "agronomy")
os.makedirs(AGRONOMY_DIR, exist_ok=True)

# 1. Penman-Monteith Evapotranspiration Engine
penman_monteith_code = '''"""
Penman-Monteith Evapotranspiration & Crop Water Requirement Engine.
Implements FAO-56 Penman-Monteith reference evapotranspiration (ET0)
and crop evapotranspiration (ETc) algorithms.
"""

import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ClimateData:
    temp_min_c: float
    temp_max_c: float
    temp_mean_c: float
    relative_humidity_pct: float
    wind_speed_m_s: float
    solar_radiation_mj_m2_day: float
    altitude_m: float = 100.0
    latitude_deg: float = 17.3850
    day_of_year: int = 180

@dataclass
class CropWaterDemand:
    reference_et0_mm_day: float
    crop_coefficient_kc: float
    crop_etc_mm_day: float
    net_irrigation_requirement_mm_day: float
    gross_irrigation_requirement_mm_day: float
    irrigation_interval_days: float
    effective_rainfall_mm_day: float

class PenmanMonteithEngine:
    """FAO-56 Penman-Monteith Evapotranspiration Calculation Engine."""
    
    SOLAR_CONSTANT_MJ_M2_MIN = 0.0820
    STEFAN_BOLTZMANN_MJ_K4_M2_DAY = 4.903e-9
    
    def __init__(self, efficiency_irrigation: float = 0.85):
        self.efficiency = efficiency_irrigation

    def calculate_saturation_vapor_pressure(self, temp_c: float) -> float:
        """Calculate saturation vapor pressure (e0) in kPa at temperature T (Celsius)."""
        return 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))

    def calculate_mean_saturation_vapor_pressure(self, t_min: float, t_max: float) -> float:
        """Calculate mean saturation vapor pressure (e_s) in kPa."""
        e_tmin = self.calculate_saturation_vapor_pressure(t_min)
        e_tmax = self.calculate_saturation_vapor_pressure(t_max)
        return (e_tmin + e_tmax) / 2.0

    def calculate_actual_vapor_pressure(self, e_s: float, rh_pct: float) -> float:
        """Calculate actual vapor pressure (e_a) in kPa."""
        return (rh_pct / 100.0) * e_s

    def calculate_slope_vapor_pressure_curve(self, t_mean: float) -> float:
        """Calculate slope of vapor pressure curve (Delta) in kPa/C."""
        return (4098.0 * (0.61078 * math.exp((17.27 * t_mean) / (t_mean + 237.3)))) / ((t_mean + 237.3) ** 2)

    def calculate_atmospheric_pressure(self, altitude_m: float) -> float:
        """Calculate atmospheric pressure (P) in kPa at altitude z (meters)."""
        return 101.3 * (((293.0 - 0.0065 * altitude_m) / 293.0) ** 5.26)

    def calculate_psychrometric_constant(self, pressure_kpa: float) -> float:
        """Calculate psychrometric constant (gamma) in kPa/C."""
        return 0.000665 * pressure_kpa

    def calculate_extraterrestrial_radiation(self, latitude_deg: float, day_of_year: int) -> float:
        """Calculate extraterrestrial radiation (Ra) in MJ/m2/day."""
        lat_rad = (math.pi / 180.0) * latitude_deg
        dr = 1.0 + 0.033 * math.cos((2.0 * math.pi / 365.0) * day_of_year)
        sol_decl = 0.409 * math.sin(((2.0 * math.pi / 365.0) * day_of_year) - 1.39)
        ws_arg = -math.tan(lat_rad) * math.tan(sol_decl)
        ws_arg = max(-1.0, min(1.0, ws_arg))
        ws = math.acos(ws_arg)
        
        ra = ((24.0 * 60.0) / math.pi) * self.SOLAR_CONSTANT_MJ_M2_MIN * dr * (
            ws * math.sin(lat_rad) * math.sin(sol_decl) +
            math.cos(lat_rad) * math.cos(sol_decl) * math.sin(ws)
        )
        return max(0.1, ra)

    def calculate_clear_sky_solar_radiation(self, ra: float, altitude_m: float) -> float:
        """Calculate clear-sky solar radiation (Rso) in MJ/m2/day."""
        return (0.75 + 2e-5 * altitude_m) * ra

    def calculate_net_solar_radiation(self, rs: float, albedo: float = 0.23) -> float:
        """Calculate net solar radiation (Rns) in MJ/m2/day."""
        return (1.0 - albedo) * rs

    def calculate_net_longwave_radiation(
        self, t_min_c: float, t_max_c: float, ea_kpa: float, rs: float, rso: float
    ) -> float:
        """Calculate net longwave radiation (Rnl) in MJ/m2/day."""
        t_min_k = t_min_c + 273.16
        t_max_k = t_max_c + 273.16
        t_term = self.STEFAN_BOLTZMANN_MJ_K4_M2_DAY * (((t_min_k ** 4) + (t_max_k ** 4)) / 2.0)
        vp_term = 0.34 - 0.14 * math.sqrt(max(0.001, ea_kpa))
        rs_ratio = min(1.0, max(0.3, rs / max(0.1, rso)))
        cloud_term = 1.35 * rs_ratio - 0.35
        return t_term * vp_term * cloud_term

    def calculate_reference_et0(self, climate: ClimateData) -> float:
        """
        Calculate FAO-56 Penman-Monteith Reference Evapotranspiration (ET0) in mm/day.
        """
        t_mean = climate.temp_mean_c
        t_min = climate.temp_min_c
        t_max = climate.temp_max_c
        rh = climate.relative_humidity_pct
        u2 = climate.wind_speed_m_s
        rs = climate.solar_radiation_mj_m2_day
        alt = climate.altitude_m
        lat = climate.latitude_deg
        doy = climate.day_of_year

        e_s = self.calculate_mean_saturation_vapor_pressure(t_min, t_max)
        e_a = self.calculate_actual_vapor_pressure(e_s, rh)
        delta = self.calculate_slope_vapor_pressure_curve(t_mean)
        patm = self.calculate_atmospheric_pressure(alt)
        gamma = self.calculate_psychrometric_constant(patm)

        ra = self.calculate_extraterrestrial_radiation(lat, doy)
        rso = self.calculate_clear_sky_solar_radiation(ra, alt)
        rns = self.calculate_net_solar_radiation(rs)
        rnl = self.calculate_net_longwave_radiation(t_min, t_max, e_a, rs, rso)
        rn = rns - rnl
        g = 0.0  # Soil heat flux density for daily timestep

        numerator = 0.408 * delta * (rn - g) + gamma * (900.0 / (t_mean + 273.0)) * u2 * (e_s - e_a)
        denominator = delta + gamma * (1.0 + 0.34 * u2)

        et0 = numerator / max(0.001, denominator)
        return max(0.1, round(et0, 3))

    def calculate_crop_water_demand(
        self,
        climate: ClimateData,
        crop_kc: float,
        rainfall_mm_day: float = 0.0,
        soil_available_water_mm: float = 100.0,
        allowable_depletion_fraction: float = 0.5
    ) -> CropWaterDemand:
        """Compute full crop water demand and irrigation schedule requirements."""
        et0 = self.calculate_reference_et0(climate)
        etc = et0 * crop_kc
        
        # USDA Soil Conservation Service Effective Rainfall Model
        if rainfall_mm_day <= 8.33:
            effective_rain = rainfall_mm_day * (125.0 - 0.2 * 3.0 * rainfall_mm_day) / 125.0
        else:
            effective_rain = 125.0 / 3.0 + 0.1 * rainfall_mm_day
        effective_rain = max(0.0, min(rainfall_mm_day, effective_rain))

        net_req = max(0.0, etc - effective_rain)
        gross_req = net_req / max(0.1, self.efficiency)

        readily_available_water = soil_available_water_mm * allowable_depletion_fraction
        irr_interval = readily_available_water / max(0.1, etc)

        return CropWaterDemand(
            reference_et0_mm_day=round(et0, 2),
            crop_coefficient_kc=round(crop_kc, 2),
            crop_etc_mm_day=round(etc, 2),
            net_irrigation_requirement_mm_day=round(net_req, 2),
            gross_irrigation_requirement_mm_day=round(gross_req, 2),
            irrigation_interval_days=round(irr_interval, 1),
            effective_rainfall_mm_day=round(effective_rain, 2)
        )
'''

with open(os.path.join(AGRONOMY_DIR, "penman_monteith_engine.py"), "w", encoding="utf-8") as f:
    f.write(penman_monteith_code)

print("Created penman_monteith_engine.py")
