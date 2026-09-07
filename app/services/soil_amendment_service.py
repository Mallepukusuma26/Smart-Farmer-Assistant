"""
Soil Amendment Service Module for Smart Farmer Assistant.

Calculates agricultural lime requirement for acidic soils, gypsum dosage for sodic soils,
organic compost decomposition requirements, and soil buffer capacity formulas.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class SoilAmendmentService:
    """
    Business service calculating chemical and organic soil amendment dosages:
    - Agricultural Lime (CaCO3) for low pH neutralization
    - Gypsum (CaSO4.2H2O) for exchangeable sodium displacement
    - Elemental Sulfur for high pH reduction
    - Organic Compost / Farmyard Manure requirements
    """

    @staticmethod
    def calculate_lime_requirement(
        current_ph: float,
        target_ph: float = 6.5,
        soil_type: str = "Loam",
        area_acres: float = 1.0,
        cce_pct: float = 90.0
    ) -> Dict[str, Any]:
        """
        Calculates agricultural limestone (CaCO3) requirement using Shoemaker-McLean-Pratt (SMP) buffer math.
        """
        if current_ph >= target_ph:
            return {
                "current_ph": current_ph,
                "target_ph": target_ph,
                "lime_required_kg_per_acre": 0.0,
                "total_lime_required_kg": 0.0,
                "status": "Optimal pH — No Liming Required"
            }

        ph_deficit = target_ph - current_ph

        # Soil buffer capacity factor by texture
        buffer_factors = {
            "sand": 400.0,
            "loamy sand": 500.0,
            "sandy loam": 700.0,
            "loam": 1000.0,
            "silt loam": 1200.0,
            "clay loam": 1500.0,
            "clay": 1800.0,
            "peaty": 2000.0
        }
        soil_lower = soil_type.lower().strip()
        factor = buffer_factors.get(soil_lower, 1000.0)

        # Base lime in kg/acre
        base_lime_kg = ph_deficit * factor
        adjusted_lime_kg = base_lime_kg * (100.0 / cce_pct)  # Adjust for Calcium Carbonate Equivalent
        total_lime_kg = adjusted_lime_kg * area_acres

        return {
            "current_ph": current_ph,
            "target_ph": target_ph,
            "ph_deficit": round(ph_deficit, 2),
            "soil_type": soil_type,
            "area_acres": area_acres,
            "lime_required_kg_per_acre": round(adjusted_lime_kg, 2),
            "total_lime_required_kg": round(total_lime_kg, 2),
            "total_lime_required_tonnes": round(total_lime_kg / 1000.0, 2),
            "application_method": "Broadcast evenly and incorporate into top 15 cm of soil 2-3 months prior to planting.",
            "estimated_cost_usd": round((total_lime_kg / 1000.0) * 45.0, 2)
        }

    @staticmethod
    def calculate_gypsum_requirement(
        esp_pct: float,
        target_esp_pct: float = 5.0,
        cec_meq_100g: float = 20.0,
        area_acres: float = 1.0,
        depth_cm: float = 15.0
    ) -> Dict[str, Any]:
        """
        Calculates Gypsum (CaSO4.2H2O) requirement for reclaiming sodic soils.
        GR = (ESP_initial - ESP_target) / 100 * CEC * Soil Mass Factor
        """
        if esp_pct <= target_esp_pct:
            return {
                "esp_pct": esp_pct,
                "target_esp_pct": target_esp_pct,
                "gypsum_required_kg_per_acre": 0.0,
                "total_gypsum_required_kg": 0.0,
                "status": "Non-Sodic Soil — No Gypsum Required"
            }

        esp_deficit = esp_pct - target_esp_pct
        # 1 meq Na/100g soil requires ~1.72 tonnes Gypsum per hectare (0.7 tonnes per acre) for 15 cm depth
        base_gypsum_tonne_acre = (esp_deficit / 100.0) * cec_meq_100g * 0.7
        total_gypsum_kg = base_gypsum_tonne_acre * 1000.0 * area_acres

        return {
            "esp_pct": esp_pct,
            "target_esp_pct": target_esp_pct,
            "gypsum_required_kg_per_acre": round(base_gypsum_tonne_acre * 1000.0, 2),
            "total_gypsum_required_kg": round(total_gypsum_kg, 2),
            "total_gypsum_required_tonnes": round(total_gypsum_kg / 1000.0, 2),
            "application_method": "Incorporate Gypsum into soil surface followed by heavy leaching irrigation.",
            "estimated_cost_usd": round((total_gypsum_kg / 1000.0) * 60.0, 2)
        }
