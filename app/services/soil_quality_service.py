"""
Soil Quality Service Module for Smart Farmer Assistant.

Provides soil physical/chemical degradation modeling, organic carbon decay math,
salinity/alkalinity risk scoring, USDA soil texture classification, and soil health index math.
"""

from typing import Dict, Any, List, Optional, Tuple
import math
import logging

logger = logging.getLogger(__name__)


class SoilQualityService:
    """
    Business service providing USDA soil texture triangle classification,
    organic carbon decomposition modeling, soil erosion risk evaluation, and soil health indexing.
    """

    @staticmethod
    def classify_usda_texture(sand_pct: float, silt_pct: float, clay_pct: float) -> str:
        """
        Classifies soil texture according to USDA Soil Texture Triangle parameters.
        """
        total = sand_pct + silt_pct + clay_pct
        if total <= 0:
            return "Loamy"

        # Normalize to 100%
        sand = (sand_pct / total) * 100
        silt = (silt_pct / total) * 100
        clay = (clay_pct / total) * 100

        if clay >= 40:
            if sand >= 45:
                return "Sandy Clay"
            elif silt >= 40:
                return "Silty Clay"
            else:
                return "Clay"
        elif clay >= 27:
            if sand >= 45:
                return "Sandy Clay Loam"
            elif silt >= 28:
                return "Silty Clay Loam"
            else:
                return "Clay Loam"
        elif clay >= 20:
            if sand >= 52:
                return "Sandy Loam"
            elif silt >= 50:
                return "Silt Loam"
            else:
                return "Loam"
        else:
            if silt + 1.5 * clay >= 15:
                if sand >= 70:
                    return "Loamy Sand"
                elif silt >= 50:
                    return "Silt"
                else:
                    return "Silt Loam"
            else:
                return "Sand"

    @staticmethod
    def calculate_organic_matter_decomposition(
        initial_soc_pct: float,
        temperature_c: float,
        rainfall_mm: float,
        tillage_factor: float = 1.0,
        years: int = 3
    ) -> Dict[str, Any]:
        """
        Models first-order organic carbon decomposition kinetics in soil over multiple years.
        SOC(t) = SOC_0 * exp(-k * t)
        """
        # Base decomposition rate constant k
        base_k = 0.03  # per year

        # Temperature response (Q10 rule)
        temp_factor = math.pow(2.0, (temperature_c - 20.0) / 10.0)
        temp_factor = max(0.5, min(temp_factor, 2.5))

        # Moisture factor
        moisture_factor = min(rainfall_mm / 1000.0, 1.5)
        moisture_factor = max(0.5, moisture_factor)

        effective_k = base_k * temp_factor * moisture_factor * tillage_factor

        annual_projections = []
        current_soc = initial_soc_pct
        for y in range(1, years + 1):
            current_soc = current_soc * math.exp(-effective_k)
            annual_projections.append({
                "year": y,
                "projected_soc_pct": round(current_soc, 3),
                "humus_loss_kg_per_acre": round((initial_soc_pct - current_soc) * 4000, 2)
            })

        return {
            "initial_soc_pct": initial_soc_pct,
            "effective_decay_rate_k": round(effective_k, 4),
            "projected_soc_pct_after_period": round(current_soc, 3),
            "annual_projections": annual_projections,
            "recommendation": "Incorporate cover crops, green manure, or compost to offset SOC decomposition."
        }

    @staticmethod
    def evaluate_salinity_alkalinity(ec_ds_m: float, ph: float, esp_pct: float = 5.0) -> Dict[str, Any]:
        """
        Evaluates soil electrical conductivity (EC) and pH for salinity, sodicity, or alkalinity risks.
        """
        is_saline = ec_ds_m > 4.0
        is_sodic = esp_pct > 15.0 or ph > 8.5
        is_alkaline = ph > 7.8

        if is_saline and is_sodic:
            classification = "Saline-Sodic Soil"
            remedy = "Apply Gypsum (CaSO4) followed by heavy leaching with good quality irrigation water."
        elif is_saline:
            classification = "Saline Soil"
            remedy = "Leach excess soluble salts using good quality water and ensure adequate field drainage."
        elif is_sodic:
            classification = "Sodic Soil"
            remedy = "Apply Gypsum or Elemental Sulfur to displace exchangeable Sodium ions."
        elif is_alkaline:
            classification = "Alkaline Soil"
            remedy = "Apply organic matter, compost, or sulfur to lower soil pH into optimal 6.0-7.2 range."
        elif ph < 5.5:
            classification = "Acidic Soil"
            remedy = "Apply Agricultural Lime (CaCO3) to neutralize soil acidity."
        else:
            classification = "Normal Productive Soil"
            remedy = "Maintain current balanced nutrient management practices."

        return {
            "ec_ds_m": ec_ds_m,
            "ph": ph,
            "esp_pct": esp_pct,
            "classification": classification,
            "recommended_remedy": remedy
        }
