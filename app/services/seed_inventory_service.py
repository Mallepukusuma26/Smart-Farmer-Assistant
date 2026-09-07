"""
Seed Inventory & Germination Quality Management Service.
Tracks seed lot batches, germination test rates, seed treatment chemicals, and sowing rate calculations.
"""

import math
from typing import Dict, List, Any

class SeedInventoryService:
    """Seed lot inventory and sowing rate calculator service."""

    def calculate_sowing_rate(
        self, target_plant_population_per_ha: float, thousand_grain_weight_g: float, germination_pct: float, purity_pct: float
    ) -> Dict[str, float]:
        """
        Sowing Rate (kg/ha) = (Target Population * TGW in g) / (Germination% * Purity% * 10,000)
        """
        germ_frac = max(0.50, min(1.0, germination_pct / 100.0))
        pur_frac = max(0.50, min(1.0, purity_pct / 100.0))
        
        sowing_rate_kg_ha = (target_plant_population_per_ha * thousand_grain_weight_g) / (germ_frac * pur_frac * 10000.0)

        return {
            "target_plant_population_ha": target_plant_population_per_ha,
            "thousand_grain_weight_g": thousand_grain_weight_g,
            "germination_pct": germination_pct,
            "purity_pct": purity_pct,
            "recommended_sowing_rate_kg_ha": round(sowing_rate_kg_ha, 2),
            "recommended_sowing_rate_kg_acre": round(sowing_rate_kg_ha * 0.404686, 2)
        }
