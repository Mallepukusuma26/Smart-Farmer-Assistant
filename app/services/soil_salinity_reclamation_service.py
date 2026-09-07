"""
Soil Salinity Reclamation & Leaching Service Module for Smart Farmer Assistant.

Calculates Leaching Fraction (LF), Leaching Requirement (LR), Sodium Adsorption Ratio (SAR),
and Exchangeable Sodium Percentage (ESP) for saline and sodic soil reclamation.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class SoilSalinityReclamationService:
    """
    Business service calculating soil salinity leaching requirements, Sodium Adsorption Ratio (SAR),
    and irrigation water quality suitability.
    """

    @staticmethod
    def calculate_sodium_adsorption_ratio(
        na_meq_l: float,
        ca_meq_l: float,
        mg_meq_l: float
    ) -> Dict[str, Any]:
        """
        Calculates Sodium Adsorption Ratio (SAR):
        SAR = Na / sqrt((Ca + Mg) / 2)
        """
        ca_mg_sum = ca_meq_l + mg_meq_l
        if ca_mg_sum <= 0:
            sar = 0.0
        else:
            sar = na_meq_l / math.sqrt(ca_mg_sum / 2.0)

        sar = round(sar, 2)

        if sar < 3.0:
            risk = "Low Sodicity Risk"
            advice = "Safe for irrigation on all soil types."
        elif sar <= 9.0:
            risk = "Medium Sodicity Risk"
            advice = "Monitor fine-textured clay soils for permeability reduction."
        else:
            risk = "High Sodicity Risk — Soil Permeability Hazard"
            advice = "Apply Gypsum to irrigation water to increase Calcium concentration."

        return {
            "na_meq_l": na_meq_l,
            "ca_meq_l": ca_meq_l,
            "mg_meq_l": mg_meq_l,
            "sodium_adsorption_ratio_sar": sar,
            "sodicity_risk_level": risk,
            "recommendation": advice
        }

    @staticmethod
    def calculate_leaching_requirement(
        ec_irrigation_water_ds_m: float,
        ec_crop_threshold_ds_m: float = 2.0
    ) -> Dict[str, Any]:
        """
        Calculates Leaching Requirement (LR %) using FAO 29 formula:
        LR = EC_w / (5 * EC_e - EC_w)
        """
        denom = (5.0 * ec_crop_threshold_ds_m) - ec_irrigation_water_ds_m
        if denom <= 0:
            lr_pct = 50.0
        else:
            lr_pct = (ec_irrigation_water_ds_m / denom) * 100.0

        lr_pct = round(max(min(lr_pct, 50.0), 5.0), 1)

        return {
            "ec_irrigation_water_ds_m": ec_irrigation_water_ds_m,
            "ec_crop_threshold_ds_m": ec_crop_threshold_ds_m,
            "leaching_requirement_lr_pct": lr_pct,
            "additional_water_needed_pct": lr_pct,
            "explanation": f"Apply {lr_pct}% extra irrigation water above crop ETc to leach excess soluble salts below root zone."
        }
