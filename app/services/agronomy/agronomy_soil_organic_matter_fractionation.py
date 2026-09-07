"""
Agronomy Soil Organic Matter Fractionation Engine for Smart Farmer Assistant.

Quantifies particulate organic matter (POM), mineral-associated organic matter (MAOM), and active labile carbon pools.
"""

from typing import Dict, Any


class AgronomySoilOrganicMatterFractionationEngine:
    """Calculates active vs passive soil organic carbon pools and humification efficiency."""

    @staticmethod
    def calculate_som_fractions(
        total_organic_carbon_pct: float,
        clay_silt_pct: float = 45.0,
        bulk_density_g_cm3: float = 1.35
    ) -> Dict[str, Any]:
        """Fractionates SOM into labile POM and stable mineral-bound MAOM."""
        # Mineral binding capacity = 0.25 * (Clay + Silt %)
        maom_capacity_pct = min(total_organic_carbon_pct, 0.25 * (clay_silt_pct / 100.0) * 10.0)
        maom_carbon = round(min(total_organic_carbon_pct * 0.70, maom_capacity_pct), 3)
        pom_carbon = round(max(0.05, total_organic_carbon_pct - maom_carbon), 3)

        # Carbon stock in metric tons / ha for 0-20cm depth
        total_carbon_stock_t_ha = round(total_organic_carbon_pct * 0.01 * bulk_density_g_cm3 * 2000.0, 1)

        return {
            "total_organic_carbon_pct": total_organic_carbon_pct,
            "particulate_organic_carbon_pct": pom_carbon,
            "mineral_associated_carbon_pct": maom_carbon,
            "labile_active_fraction_pct": round((pom_carbon / total_organic_carbon_pct) * 100.0, 1),
            "stable_passive_fraction_pct": round((maom_carbon / total_organic_carbon_pct) * 100.0, 1),
            "total_carbon_stock_t_ha_top20cm": total_carbon_stock_t_ha
        }
