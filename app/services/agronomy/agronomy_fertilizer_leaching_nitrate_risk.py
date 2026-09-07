"""
Agronomy Fertilizer Leaching & Nitrate Risk Engine for Smart Farmer Assistant.

Models nitrate-nitrogen leaching potential based on soil texture, rainfall intensity, and nitrogen application rate.
"""

from typing import Dict, Any


class AgronomyFertilizerLeachingNitrateRiskEngine:
    """Estimates nitrate (NO3-N) leaching vulnerability and groundwater contamination risk."""

    @staticmethod
    def calculate_nitrate_leaching_risk(
        nitrogen_applied_kg_ha: float,
        irrigation_plus_rainfall_mm: float,
        soil_type: str = "Sandy Loam",
        clay_pct: float = 15.0
    ) -> Dict[str, Any]:
        """Calculates leaching fraction and estimated NO3-N loss in kg/ha."""
        # Drainage factor increases with coarser soil texture
        if "sand" in soil_type.lower():
            drainage_factor = 0.45
        elif "clay" in soil_type.lower():
            drainage_factor = 0.12
        else:
            drainage_factor = 0.25

        leaching_volume_mm = max(0.0, irrigation_plus_rainfall_mm - 150.0) * drainage_factor
        leached_n_kg_ha = round(nitrogen_applied_kg_ha * (leaching_volume_mm / 300.0) * (1.0 - (clay_pct / 100.0)), 2)
        leached_n_kg_ha = max(0.0, min(nitrogen_applied_kg_ha * 0.5, leached_n_kg_ha))

        risk_level = "High Risk" if leached_n_kg_ha > 30.0 else ("Moderate Risk" if leached_n_kg_ha > 12.0 else "Low Risk")

        return {
            "nitrogen_applied_kg_ha": nitrogen_applied_kg_ha,
            "soil_type": soil_type,
            "estimated_leaching_volume_mm": round(leaching_volume_mm, 1),
            "estimated_nitrate_loss_kg_ha": leached_n_kg_ha,
            "nitrate_leaching_risk_level": risk_level,
            "mitigation_advice": "Split nitrogen into 3-4 top-dressings and use slow-release urea or neem-coated urea." if leached_n_kg_ha > 15.0 else "Leaching risk is within safe environmental bounds."
        }
