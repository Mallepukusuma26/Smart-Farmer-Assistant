"""
Agronomy Crop Canopy Leaf Area Index (LAI) Engine for Smart Farmer Assistant.

Models leaf area index progression, light extinction coefficients, and canopy closure percentage.
"""

import math
from typing import Dict, Any


class AgronomyCropCanopyLAIEngine:
    """Calculates leaf area index (LAI), light interception, and photosynthetically active radiation (PAR)."""

    @staticmethod
    def calculate_lai_and_par_interception(
        plant_density_per_m2: float,
        leaf_count_per_plant: float,
        avg_leaf_area_cm2: float,
        extinction_coef_k: float = 0.65,
        incident_par_mj_m2: float = 12.0
    ) -> Dict[str, Any]:
        """Computes total canopy LAI, fraction of intercepted PAR (fPAR), and absorbed PAR."""
        total_leaf_area_m2 = (plant_density_per_m2 * leaf_count_per_plant * avg_leaf_area_cm2) / 10000.0
        lai = round(max(0.1, min(10.0, total_leaf_area_m2)), 2)

        # Beer-Lambert law for light extinction: fPAR = 1 - exp(-K * LAI)
        f_par = round(1.0 - math.exp(-extinction_coef_k * lai), 4)
        absorbed_par = round(incident_par_mj_m2 * f_par, 2)

        return {
            "leaf_area_index": lai,
            "extinction_coefficient_k": extinction_coef_k,
            "fraction_par_intercepted": f_par,
            "par_intercepted_pct": round(f_par * 100.0, 1),
            "absorbed_par_mj_m2": absorbed_par,
            "canopy_closure_status": "Complete Canopy" if lai >= 3.5 else ("Partial Canopy" if lai >= 1.5 else "Initial Canopy")
        }
