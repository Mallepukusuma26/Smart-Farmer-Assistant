"""
Agronomy Soil Phosphorus Fixation Capacity Engine for Smart Farmer Assistant.

Models phosphorus sorption isotherms, P-fixation capacity in acidic/alkaline soils, and Olsen/Bray P availability.
"""

from typing import Dict, Any


class AgronomySoilPhosphorusFixationEngine:
    """Calculates phosphorus sorption capacity and phosphate fertilizer availability factor."""

    @staticmethod
    def calculate_p_fixation_and_availability(
        soil_ph: float,
        clay_content_pct: float,
        extractable_p_ppm: float,
        applied_p_kg_ha: float = 50.0
    ) -> Dict[str, Any]:
        """Calculates P fixation percentage based on pH extremes and aluminum/calcium precipitation."""
        # P availability is max around pH 6.2 - 7.2
        if soil_ph < 6.0:
            # Aluminum & Iron phosphate precipitation
            fixation_pct = round(min(85.0, 35.0 + (6.0 - soil_ph) * 15.0 + (clay_content_pct * 0.3)), 1)
            mechanism = "Fe / Al Oxide Chemisorption (Acidic Soil Fixation)"
        elif soil_ph > 7.5:
            # Calcium phosphate precipitation
            fixation_pct = round(min(85.0, 30.0 + (soil_ph - 7.5) * 18.0 + (clay_content_pct * 0.2)), 1)
            mechanism = "Calcium Phosphate Precipitation (Alkaline Soil Fixation)"
        else:
            fixation_pct = round(max(15.0, 20.0 + (clay_content_pct * 0.2)), 1)
            mechanism = "Optimal Availability Zone"

        effective_p_available_kg_ha = round(applied_p_kg_ha * (1.0 - (fixation_pct / 100.0)), 2)

        return {
            "soil_ph": soil_ph,
            "clay_content_pct": clay_content_pct,
            "applied_p_kg_ha": applied_p_kg_ha,
            "p_fixation_pct": fixation_pct,
            "primary_fixation_mechanism": mechanism,
            "net_effective_available_p_kg_ha": effective_p_available_kg_ha,
            "recommendation": "Band placement of phosphatic fertilizers near roots or use mycorrhizal inoculants to improve P recovery." if fixation_pct > 50.0 else "Phosphate availability is satisfactory."
        }
