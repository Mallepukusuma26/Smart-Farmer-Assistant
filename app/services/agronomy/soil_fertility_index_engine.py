"""
Soil Fertility Index (SFI) Engine.
Integrates chemical, physical, and biological soil metrics into a single unified rating score (0-100).
"""

from typing import Dict, Any

class SoilFertilityIndexEngine:
    """Integrated multi-parameter soil fertility index calculator."""

    def calculate_sfi(
        self,
        ph: float,
        om_pct: float,
        n_ppm: float,
        p_ppm: float,
        k_ppm: float,
        cec: float,
        ec_ds_m: float
    ) -> Dict[str, Any]:
        """Compute weighted Soil Fertility Index score (0-100)."""
        # pH score (optimal 6.0 - 7.5)
        if 6.0 <= ph <= 7.5:
            s_ph = 100.0
        else:
            s_ph = max(0.0, 100.0 - abs(ph - 6.75) * 30.0)

        # Organic matter score (optimal > 3.0%)
        s_om = min(100.0, (om_pct / 3.0) * 100.0)

        # NPK scores
        s_n = min(100.0, (n_ppm / 150.0) * 100.0)
        s_p = min(100.0, (p_ppm / 25.0) * 100.0)
        s_k = min(100.0, (k_ppm / 180.0) * 100.0)

        # Weighting: OM=25%, pH=20%, N=15%, P=15%, K=15%, CEC=10%
        sfi = (s_om * 0.25) + (s_ph * 0.20) + (s_n * 0.15) + (s_p * 0.15) + (s_k * 0.15) + (min(100.0, (cec/20.0)*100) * 0.10)
        sfi = round(max(0.0, min(100.0, sfi)), 1)

        return {
            "soil_fertility_index": sfi,
            "fertility_class": "Very High" if sfi >= 85 else ("High" if sfi >= 70 else ("Moderate" if sfi >= 50 else "Low")),
            "component_scores": {
                "ph_score": round(s_ph, 1),
                "organic_matter_score": round(s_om, 1),
                "nitrogen_score": round(s_n, 1),
                "phosphorus_score": round(s_p, 1),
                "potassium_score": round(s_k, 1)
            }
        }
