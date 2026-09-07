"""
Agronomy Root Respiration Engine for Smart Farmer Assistant.

Calculates root respiration rate and oxygen consumption based on soil temperature and porosity.
"""
from typing import Dict, Any

class AgronomyRootRespirationEngine:
    @staticmethod
    def calculate_root_respiration(root_mass_g_m2: float, soil_temp_c: float, oxygen_concentration_pct: float) -> Dict[str, Any]:
        temp_factor = 2.0 ** ((soil_temp_c - 20.0) / 10.0)
        o2_factor = max(0.1, min(1.0, oxygen_concentration_pct / 21.0))
        respiration_rate_mg_o2_m2_hr = round(root_mass_g_m2 * 0.15 * temp_factor * o2_factor, 2)
        return {
            'root_mass_g_m2': root_mass_g_m2,
            'soil_temp_c': soil_temp_c,
            'oxygen_concentration_pct': oxygen_concentration_pct,
            'respiration_rate_mg_o2_m2_hr': respiration_rate_mg_o2_m2_hr,
            'aeration_status': 'Optimal' if oxygen_concentration_pct > 15.0 else 'Hypoxic Risk'
        }
