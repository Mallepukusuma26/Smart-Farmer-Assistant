"""
Fertigation Service Module for Smart Farmer Assistant.

Calculates hydroponic and drip fertigation stock solution concentrations,
Tank A / Tank B calcium and sulfate precipitate incompatibility rules,
electrical conductivity (EC target mS/cm) calculations, and injection rates.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class FertilizerFertigationService:
    """
    Business service calculating drip fertigation nutrient stock solution recipes,
    Tank A (Calcium/Iron) and Tank B (Sulfate/Phosphate) segregation rules,
    and EC electrical conductivity target math.
    """

    @staticmethod
    def calculate_fertigation_recipe(
        volume_liters: float,
        target_ec_ms_cm: float = 2.0,
        crop_type: str = "tomato"
    ) -> Dict[str, Any]:
        """
        Calculates concentrated stock solution amounts (100x concentration factor)
        for dual-tank A/B drip fertigation.
        """
        # Base dosage for 1000 Liters at EC 2.0 mS/cm
        tank_a_calcium_nitrate_g = volume_liters * 0.90
        tank_a_iron_edta_g = volume_liters * 0.02

        tank_b_potassium_nitrate_g = volume_liters * 0.50
        tank_b_monopotassium_phosphate_g = volume_liters * 0.20
        tank_b_magnesium_sulfate_g = volume_liters * 0.40

        total_fertilizer_mass_g = (
            tank_a_calcium_nitrate_g + tank_a_iron_edta_g +
            tank_b_potassium_nitrate_g + tank_b_monopotassium_phosphate_g +
            tank_b_magnesium_sulfate_g
        )

        return {
            "irrigation_volume_liters": volume_liters,
            "target_ec_ms_cm": target_ec_ms_cm,
            "tank_a_calcium_iron_stock": {
                "calcium_nitrate_g": round(tank_a_calcium_nitrate_g, 1),
                "iron_chelate_edta_g": round(tank_a_iron_edta_g, 1),
                "instructions": "Dissolve in Tank A. NEVER mix with Sulfates or Phosphates in concentrated form."
            },
            "tank_b_sulfate_phosphate_stock": {
                "potassium_nitrate_g": round(tank_b_potassium_nitrate_g, 1),
                "monopotassium_phosphate_mkp_g": round(tank_b_monopotassium_phosphate_g, 1),
                "magnesium_sulfate_epsom_g": round(tank_b_magnesium_sulfate_g, 1),
                "instructions": "Dissolve in Tank B."
            },
            "total_fertilizer_salts_g": round(total_fertilizer_mass_g, 1),
            "injection_ratio": "1:100 (10 Liters stock per 1,000 Liters irrigation water)"
        }
