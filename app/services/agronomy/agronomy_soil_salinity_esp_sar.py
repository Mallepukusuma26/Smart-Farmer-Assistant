"""
Agronomy Soil Salinity ESP & SAR Engine for Smart Farmer Assistant.

Calculates Sodium Adsorption Ratio (SAR), Exchangeable Sodium Percentage (ESP), and soil sodicity classification.
"""

import math
from typing import Dict, Any


class AgronomySoilSalinityESPSAREngine:
    """Calculates SAR, ESP, and soil sodicity reclamation gypsum requirements."""

    @staticmethod
    def calculate_sar_and_esp(
        na_meq_l: float,
        ca_meq_l: float,
        mg_meq_l: float,
        ec_ds_m: float = 1.8
    ) -> Dict[str, Any]:
        """
        SAR = Na / sqrt((Ca + Mg) / 2)
        ESP = (1.54 * SAR) / (1 + 0.015 * SAR)
        """
        denom = math.sqrt((ca_meq_l + mg_meq_l) / 2.0) if (ca_meq_l + mg_meq_l) > 0 else 1.0
        sar = round(na_meq_l / denom, 2)
        esp = round((1.54 * sar) / (1.0 + (0.015 * sar)), 2)

        # USDA Classification: Normal, Saline, Sodic, Saline-Sodic
        if ec_ds_m > 4.0 and esp < 15.0:
            classification = "Saline Soil"
        elif ec_ds_m <= 4.0 and esp >= 15.0:
            classification = "Sodic Soil (Requires Gypsum Reclamation)"
        elif ec_ds_m > 4.0 and esp >= 15.0:
            classification = "Saline-Sodic Soil"
        else:
            classification = "Normal Non-Saline Non-Sodic Soil"

        gypsum_requirement_tons_acre = round(max(0.0, (esp - 10.0) * 0.15), 2) if esp > 10.0 else 0.0

        return {
            "sodium_adsorption_ratio_sar": sar,
            "exchangeable_sodium_pct_esp": esp,
            "electrical_conductivity_ec_ds_m": ec_ds_m,
            "usda_soil_classification": classification,
            "gypsum_reclamation_tons_per_acre": gypsum_requirement_tons_acre
        }
