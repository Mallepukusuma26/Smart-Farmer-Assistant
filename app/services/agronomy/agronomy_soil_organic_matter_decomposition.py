"""
Agronomy Soil Organic Matter Decomposition Engine for Smart Farmer Assistant.

Calculates turnover rate of labile and recalcitrant organic carbon pools.
"""
from typing import Dict, Any

class AgronomySoilOrganicMatterDecompositionEngine:
    @staticmethod
    def calculate_som_turnover(total_soc_g_kg: float, c_n_ratio: float, clay_pct: float) -> Dict[str, Any]:
        k_decomp = 0.0008 * (30.0 / max(10.0, c_n_ratio)) * (1.0 - (clay_pct * 0.005))
        annual_humus_min_kg_ha = round(total_soc_g_kg * 2000.0 * k_decomp, 1)
        return {
            'total_soc_g_kg': total_soc_g_kg,
            'c_n_ratio': c_n_ratio,
            'clay_pct': clay_pct,
            'k_decomposition': round(k_decomp, 5),
            'annual_mineralized_n_kg_ha': round(annual_humus_min_kg_ha * 0.08, 1)
        }
