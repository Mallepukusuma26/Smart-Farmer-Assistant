"""
Soil Fertility Mapping Service Module for Smart Farmer Assistant.

Provides spatial nutrient variability indexing, grid sampling interpolation, and fertility zonation.
"""

from typing import Dict, Any, List, Optional


class SoilFertilityMappingService:
    """Computes spatial soil fertility index (SFI 0-100) and nutrient zonation for precision field management."""

    def calculate_soil_fertility_index(
        self,
        ph: float,
        nitrogen_ppm: float,
        phosphorus_ppm: float,
        potassium_ppm: float,
        organic_carbon_pct: float,
        ec_ds_m: float = 1.2
    ) -> Dict[str, Any]:
        """
        SFI = (pH_Score * 0.20) + (N_Score * 0.25) + (P_Score * 0.20) + (K_Score * 0.15) + (OC_Score * 0.20)
        """
        ph_score = 100.0 - (abs(ph - 6.8) * 20.0)
        ph_score = max(10.0, min(100.0, ph_score))

        n_score = min(100.0, (nitrogen_ppm / 200.0) * 100.0)
        p_score = min(100.0, (phosphorus_ppm / 65.0) * 100.0)
        k_score = min(100.0, (potassium_ppm / 220.0) * 100.0)
        oc_score = min(100.0, (organic_carbon_pct / 0.85) * 100.0)

        sfi = round((ph_score * 0.20) + (n_score * 0.25) + (p_score * 0.20) + (k_score * 0.15) + (oc_score * 0.20), 1)

        zonation = "High Fertility Zone (Tier 1)" if sfi >= 80.0 else (
            "Medium Fertility Zone (Tier 2)" if sfi >= 60.0 else "Low Fertility Zone (Requires Soil Amendment)"
        )

        return {
            "soil_fertility_index_sfi": sfi,
            "fertility_zonation": zonation,
            "sub_scores": {
                "ph_balance_score": round(ph_score, 1),
                "nitrogen_availability_score": round(n_score, 1),
                "phosphorus_availability_score": round(p_score, 1),
                "potassium_availability_score": round(k_score, 1),
                "organic_carbon_score": round(oc_score, 1)
            }
        }
