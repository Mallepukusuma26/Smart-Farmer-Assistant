"""
Agronomy Livestock Forage Carrying Capacity Engine for Smart Farmer Assistant.

Models forage dry matter production (kg DM/ha), animal unit month (AUM), and pasture stocking rate.
"""

from typing import Dict, Any


class AgronomyLivestockForageCarryingCapacityEngine:
    """Calculates pasture carrying capacity in Animal Unit Months (AUM) and grazing stocking rates."""

    @staticmethod
    def calculate_pasture_stocking_rate(
        pasture_area_ha: float,
        annual_forage_yield_kg_dm_ha: float,
        avg_animal_weight_kg: float = 450.0,
        harvest_efficiency_pct: float = 50.0,
        grazing_days: float = 180.0
    ) -> Dict[str, Any]:
        """
        1 Animal Unit (AU) = 450 kg cow consuming 2.5% body weight in DM daily = 11.25 kg DM/day = 337.5 kg DM/month.
        """
        daily_intake_kg_dm = avg_animal_weight_kg * 0.025
        total_forage_produced_kg = pasture_area_ha * annual_forage_yield_kg_dm_ha
        usable_forage_kg = total_forage_produced_kg * (harvest_efficiency_pct / 100.0)

        total_intake_per_animal_period = daily_intake_kg_dm * grazing_days
        max_head_count = int(usable_forage_kg / total_intake_per_animal_period) if total_intake_per_animal_period > 0 else 0

        aum_total = round(usable_forage_kg / 337.5, 1)

        return {
            "pasture_area_ha": pasture_area_ha,
            "annual_forage_yield_kg_dm_ha": annual_forage_yield_kg_dm_ha,
            "total_usable_forage_kg_dm": round(usable_forage_kg, 1),
            "animal_unit_months_aum": aum_total,
            "recommended_stocking_head_count": max_head_count,
            "stocking_density_head_per_ha": round(max_head_count / max(0.1, pasture_area_ha), 2),
            "pasture_management_rule": "Maintain 50% stubble height ('Take half, leave half') to preserve root reserves and prevent erosion."
        }
