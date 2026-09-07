"""
Crop Health & Plant Protection Service Module for Smart Farmer Assistant.

Manages crop physiological health indexing, canopy cover estimation,
chlorophyll Index math (SPAD equivalent), stress symptom diagnosis, and growth stage tracking.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class CropHealthService:
    """
    Business service calculating crop health index, canopy cover percentage,
    chlorophyll status, and abiotic stress (drought, salinity, temperature) detection.
    """

    @staticmethod
    def calculate_crop_health_index(
        spad_chlorophyll: float,
        canopy_cover_pct: float,
        leaf_area_index_lai: float,
        water_stress_index: float = 0.2
    ) -> Dict[str, Any]:
        """
        Calculates composite Crop Health Index (CHI) from SPAD chlorophyll, LAI, and canopy cover.
        """
        norm_spad = min(spad_chlorophyll / 50.0, 1.0) * 35.0
        norm_canopy = (canopy_cover_pct / 100.0) * 35.0
        norm_lai = min(leaf_area_index_lai / 6.0, 1.0) * 30.0

        raw_chi = norm_spad + norm_canopy + norm_lai
        chi = round(raw_chi * (1.0 - max(min(water_stress_index, 0.5), 0.0)), 2)

        if chi >= 80.0:
            rating = "Vigorous Healthy Crop"
            action = "Maintain regular irrigation and nutrient schedule."
        elif chi >= 60.0:
            rating = "Moderate Crop Health"
            action = "Check for mild nutrient deficiency or early water stress."
        elif chi >= 40.0:
            rating = "Stressed Crop"
            action = "Apply emergency irrigation and foliar NPK / micronutrient spray."
        else:
            rating = "Severe Crop Distress"
            action = "Consult agricultural advisor immediately for disease/pest and soil inspection."

        return {
            "crop_health_index_chi": chi,
            "spad_chlorophyll_reading": spad_chlorophyll,
            "canopy_cover_pct": canopy_cover_pct,
            "leaf_area_index_lai": leaf_area_index_lai,
            "water_stress_index": water_stress_index,
            "health_rating": rating,
            "recommended_action": action
        }
