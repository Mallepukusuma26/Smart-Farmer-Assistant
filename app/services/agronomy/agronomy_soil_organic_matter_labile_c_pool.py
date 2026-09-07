"""
Agronomy Soil Organic Matter Labile C Pool Engine for Smart Farmer Assistant.

Models Permanganate Oxidizable Carbon (POXC / Active Carbon in mg/kg) and soil biological health index.
"""

from typing import Dict, Any


class AgronomySoilLabileCarbonEngine:
    """Calculates Active Carbon (POXC mg/kg) and biological soil fertility responsiveness."""

    @staticmethod
    def calculate_active_carbon_poxc(
        total_organic_carbon_pct: float,
        clay_pct: float = 20.0,
        management_system: str = "No-Till Cover Crop"
    ) -> Dict[str, Any]:
        """
        POXC (mg/kg) ~ 450 + (350 * SOC %) + Management Bonus
        """
        bonus = 150.0 if "no-till" in management_system.lower() else (50.0 if "reduced" in management_system.lower() else 0.0)
        poxc_mg_kg = round(max(150.0, 400.0 + (320.0 * total_organic_carbon_pct) + bonus), 1)

        # POXC / SOC ratio
        soc_mg_kg = total_organic_carbon_pct * 10000.0
        active_c_ratio_pct = round((poxc_mg_kg / max(1.0, soc_mg_kg)) * 100.0, 2)

        health_rating = "Excellent Active Carbon Pool (High Biological Activity)" if poxc_mg_kg >= 750.0 else (
            "Good Active Carbon Pool" if poxc_mg_kg >= 450.0 else "Low Active Carbon (Degraded Soil Biology)"
        )

        return {
            "total_organic_carbon_pct": total_organic_carbon_pct,
            "permanganate_oxidizable_carbon_poxc_mg_kg": poxc_mg_kg,
            "active_carbon_ratio_pct": active_c_ratio_pct,
            "biological_health_rating": health_rating,
            "soil_management_practice": management_system
        }
