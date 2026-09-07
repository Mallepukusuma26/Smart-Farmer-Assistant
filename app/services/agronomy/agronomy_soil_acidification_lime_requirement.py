"""
Agronomy Soil Acidification Lime Requirement Engine for Smart Farmer Assistant.

Models Shoemaker-McLean-Pratt (SMP) buffer pH method for agricultural limestone requirement (tons/acre).
"""

from typing import Dict, Any


class AgronomySoilLimeRequirementEngine:
    """Calculates SMP buffer lime requirement (tons CaCO3/acre) to elevate acid soil pH to target 6.5."""

    @staticmethod
    def calculate_lime_requirement(
        water_ph: float,
        smp_buffer_ph: float,
        target_ph: float = 6.5,
        area_acres: float = 1.0
    ) -> Dict[str, Any]:
        """
        SMP Buffer Lime Requirement (Tons/acre 100% CCE):
        Lime Tons = (6.8 - SMP Buffer pH) * 4.2
        """
        if water_ph >= target_ph:
            return {
                "soil_ph": water_ph,
                "lime_required_tons_per_acre": 0.0,
                "liming_status": "No liming required — soil pH is already optimal."
            }

        smp_deficit = max(0.1, 6.8 - smp_buffer_ph)
        lime_tons_acre = round(smp_deficit * 4.2, 2)
        total_lime_tons = round(lime_tons_acre * area_acres, 2)

        return {
            "water_ph": water_ph,
            "smp_buffer_ph": smp_buffer_ph,
            "target_ph": target_ph,
            "lime_required_tons_per_acre": lime_tons_acre,
            "total_lime_required_tons": total_lime_tons,
            "application_advice": "Broadcast agricultural limestone (CaCO3) evenly and disk into top 15cm soil 2-3 months prior to sowing."
        }
