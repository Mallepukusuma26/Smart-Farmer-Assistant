"""
Agronomy Crop Lodging & Stem Strength Model for Smart Farmer Assistant.

Models cereal crop stem bending moment, wind speed lodging risk, and Plant Growth Regulator (PGR) dosing.
"""

import math
from typing import Dict, Any


class AgronomyCropLodgingModelEngine:
    """Calculates stem safety factor against wind lodging and PGR lodging reduction."""

    @staticmethod
    def calculate_lodging_risk(
        crop_height_cm: float,
        stem_diameter_mm: float,
        wind_gust_km_h: float = 40.0,
        nitrogen_applied_kg_ha: float = 160.0
    ) -> Dict[str, Any]:
        """
        Bending Moment = Height * Wind Force
        Excess Nitrogen increases stem internode length and lodging risk.
        """
        slenderness_ratio = crop_height_cm / max(1.0, stem_diameter_mm * 10.0)
        n_excess_factor = max(1.0, nitrogen_applied_kg_ha / 120.0)

        lodging_index = round(min(100.0, (slenderness_ratio * 35.0 * n_excess_factor) + (wind_gust_km_h * 0.8)), 1)

        lodging_risk_class = "HIGH LODGING RISK — PRE-HARVEST STEM FLATTENING PROBABLE" if lodging_index >= 65.0 else (
            "Moderate Lodging Risk" if lodging_index >= 35.0 else "Low Lodging Risk (Sturdy Stem)"
        )

        return {
            "crop_height_cm": crop_height_cm,
            "stem_diameter_mm": stem_diameter_mm,
            "slenderness_ratio": round(slenderness_ratio, 2),
            "wind_gust_km_h": wind_gust_km_h,
            "lodging_risk_index_100": lodging_index,
            "lodging_risk_classification": lodging_risk_class,
            "pgr_recommendation": "Apply Chlormequat Chloride (CCC) or Trinexapac-ethyl at stem elongation (Zadoks 31) to shorten lower internodes." if lodging_index > 45.0 else "Stem strength is adequate."
        }
