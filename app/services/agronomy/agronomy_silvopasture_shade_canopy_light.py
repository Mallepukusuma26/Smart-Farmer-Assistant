"""
Agronomy Silvopasture Shade Canopy & Light Engine for Smart Farmer Assistant.

Models agroforestry tree canopy light transmissivity (PAR %), understory grass photosynthesis, and timber density.
"""

import math
from typing import Dict, Any


class AgronomySilvopastureShadeCanopyEngine:
    """Calculates tree canopy shade transmissivity %, understory forage growth reduction, and optimum tree thinning."""

    @staticmethod
    def calculate_silvopasture_light_transmissivity(
        tree_stems_per_ha: float,
        avg_crown_diameter_m: float,
        pruning_height_m: float = 3.5,
        open_par_mj_m2: float = 16.0
    ) -> Dict[str, Any]:
        """Calculates percentage of full sunlight reaching understory forage crops in silvopasture systems."""
        single_crown_area_m2 = math.pi * ((avg_crown_diameter_m / 2.0) ** 2)
        total_crown_area_ha = (tree_stems_per_ha * single_crown_area_m2) / 10000.0

        canopy_cover_pct = round(min(90.0, total_crown_area_ha * 100.0), 1)
        light_transmissivity_pct = round(100.0 - (canopy_cover_pct * 0.75), 1)

        understory_par_mj_m2 = round(open_par_mj_m2 * (light_transmissivity_pct / 100.0), 2)
        forage_yield_relative_pct = round(min(100.0, light_transmissivity_pct * 1.05), 1)

        thinning_advice = "THIN TREE CANOPY — Tree density > 50% cover reduces forage dry matter yield significantly." if canopy_cover_pct > 50.0 else "Optimal Silvopasture Light Balance"

        return {
            "tree_stems_per_ha": tree_stems_per_ha,
            "avg_crown_diameter_m": avg_crown_diameter_m,
            "tree_canopy_cover_pct": canopy_cover_pct,
            "understory_light_transmissivity_pct": light_transmissivity_pct,
            "understory_par_mj_m2": understory_par_mj_m2,
            "relative_forage_yield_pct": forage_yield_relative_pct,
            "silvopasture_management_recommendation": thinning_advice
        }
