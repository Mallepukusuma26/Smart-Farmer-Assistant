"""
Agronomy Nitrogen Leaching Loss Engine for Smart Farmer Assistant.

Estimates nitrate leaching potential based on rainfall, soil drainage, and soil N pool.
"""
from typing import Dict, Any

class AgronomyNitrogenLeachingLossEngine:
    @staticmethod
    def estimate_n_leaching(applied_n_kg_ha: float, rainfall_mm: float, drainage_capacity: str, soil_sand_pct: float) -> Dict[str, Any]:
        leaching_coeff = 0.05
        if soil_sand_pct > 60:
            leaching_coeff += 0.15
        if drainage_capacity.lower() in ['excessive', 'high']:
            leaching_coeff += 0.10
        if rainfall_mm > 100:
            leaching_coeff += (rainfall_mm - 100) * 0.002
        leaching_coeff = min(0.60, max(0.02, leaching_coeff))
        estimated_n_lost_kg_ha = round(applied_n_kg_ha * leaching_coeff, 2)
        return {
            'applied_n_kg_ha': applied_n_kg_ha,
            'leaching_coefficient': round(leaching_coeff, 3),
            'estimated_n_lost_kg_ha': estimated_n_lost_kg_ha,
            'retained_n_kg_ha': round(applied_n_kg_ha - estimated_n_lost_kg_ha, 2),
            'mitigation_advice': 'Split application of nitrogen recommended' if leaching_coeff > 0.25 else 'Standard nitrogen management adequate'
        }
