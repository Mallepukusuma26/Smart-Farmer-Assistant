"""
Agronomy Soil Aggregate Slaking Risk Engine for Smart Farmer Assistant.

Models wet aggregate stability (MWD in mm), slaking vulnerability under heavy rainfall, and crusting risk.
"""

from typing import Dict, Any


class AgronomySoilAggregateSlakingEngine:
    """Calculates Mean Weight Diameter (MWD mm) of soil aggregates and surface crusting susceptibility."""

    @staticmethod
    def calculate_aggregate_slaking_risk(
        organic_matter_pct: float,
        clay_pct: float,
        sodium_esp_pct: float = 3.0,
        tillage_intensity: str = "Conventional Tillage"
    ) -> Dict[str, Any]:
        """
        MWD = 0.5 + (0.3 * SOM %) + (0.02 * Clay %) - (0.05 * ESP %)
        """
        mwd_mm = round(max(0.2, 0.5 + (0.3 * organic_matter_pct) + (0.02 * clay_pct) - (0.05 * sodium_esp_pct)), 2)

        slaking_risk = "High Slaking & Surface Crusting Risk" if mwd_mm < 1.0 else (
            "Moderate Aggregate Stability" if mwd_mm < 2.0 else "Stable Water-Resistant Soil Structure"
        )

        return {
            "organic_matter_pct": organic_matter_pct,
            "clay_pct": clay_pct,
            "mean_weight_diameter_mwd_mm": mwd_mm,
            "slaking_risk_evaluation": slaking_risk,
            "soil_conservation_advice": "Transition to No-Till / Reduced Tillage and apply cover crop residue to prevent rainfall drop impact slaking." if mwd_mm < 1.5 else "Soil structure exhibits excellent water stability."
        }
