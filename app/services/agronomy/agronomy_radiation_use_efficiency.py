"""
Agronomy Radiation Use Efficiency (RUE) Engine for Smart Farmer Assistant.

Calculates biomass accumulation per unit of intercepted solar radiation (g/MJ).
"""
from typing import Dict, Any

class AgronomyRadiationUseEfficiencyEngine:
    @staticmethod
    def calculate_biomass_production(intercepted_solar_rad_mj_m2: float, rue_g_mj: float = 1.45, stress_factor: float = 1.0) -> Dict[str, Any]:
        actual_rue = rue_g_mj * min(1.0, max(0.2, stress_factor))
        produced_biomass_g_m2 = round(intercepted_solar_rad_mj_m2 * actual_rue, 2)
        produced_biomass_kg_ha = round(produced_biomass_g_m2 * 10.0, 1)
        return {
            'potential_rue_g_mj': rue_g_mj,
            'actual_rue_g_mj': round(actual_rue, 3),
            'biomass_g_m2': produced_biomass_g_m2,
            'biomass_kg_ha': produced_biomass_kg_ha,
            'stress_penalty_pct': round((1.0 - stress_factor) * 100, 1)
        }
