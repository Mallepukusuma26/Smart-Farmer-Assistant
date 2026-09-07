"""
Agronomy Solar Irradiance Calculator Engine for Smart Farmer Assistant.

Calculates clear-sky solar irradiance and photoperiod for crop growth modeling.
"""
import math
from typing import Dict, Any

class AgronomySolarIrradianceCalculatorEngine:
    @staticmethod
    def calculate_daily_extraterrestrial_radiation(latitude_deg: float, day_of_year: int) -> Dict[str, Any]:
        lat_rad = math.radians(latitude_deg)
        declination = 0.409 * math.sin((2 * math.pi / 365 * day_of_year) - 1.39)
        ws = math.acos(-math.tan(lat_rad) * math.tan(declination))
        dr = 1 + 0.033 * math.cos(2 * math.pi / 365 * day_of_year)
        ra = (24 * 60 / math.pi) * 0.0820 * dr * (ws * math.sin(lat_rad) * math.sin(declination) + math.cos(lat_rad) * math.cos(declination) * math.sin(ws))
        day_length_hours = round(2 * ws * 24 / (2 * math.pi), 1)
        return {
            'latitude_deg': latitude_deg,
            'day_of_year': day_of_year,
            'extraterrestrial_radiation_mj_m2_day': round(ra, 2),
            'day_length_hours': day_length_hours
        }
