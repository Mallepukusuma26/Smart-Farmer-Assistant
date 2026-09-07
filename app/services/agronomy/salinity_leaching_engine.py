"""
Soil Salinity Reclamation & Leaching Requirement Engine.
Implements US Salinity Laboratory formulas for ECe leaching requirements
and Gypsum requirements for Sodic soil reclamation.
"""

from typing import Dict, Any

class SalinityLeachingEngine:
    """Soil and water salinity reclamation calculator."""

    def calculate_leaching_requirement(
        self, ec_irrigation_ds_m: float, target_ec_soil_ds_m: float = 4.0
    ) -> Dict[str, float]:
        """
        Leaching Requirement LR = ECw / (5 * ECe_target - ECw)
        """
        ec_w = ec_irrigation_ds_m
        ec_e = target_ec_soil_ds_m

        denom = max(0.1, (5.0 * ec_e) - ec_w)
        lr_fraction = ec_w / denom
        lr_fraction = max(0.05, min(0.50, lr_fraction))

        return {
            "irrigation_water_ec_ds_m": ec_w,
            "target_soil_ec_ds_m": ec_e,
            "leaching_requirement_fraction": round(lr_fraction, 3),
            "leaching_requirement_pct": round(lr_fraction * 100.0, 1),
            "additional_water_needed_pct": round((lr_fraction / (1.0 - lr_fraction)) * 100.0, 1)
        }

    def calculate_gypsum_requirement(
        self, current_esp_pct: float, target_esp_pct: float, cec_meq_100g: float, soil_depth_cm: float = 30.0
    ) -> Dict[str, float]:
        """
        Calculate pure Gypsum (CaSO4.2H2O) requirement in metric tons/ha for sodic soil reclamation.
        GR (tons/ha) = 0.086 * CEC * (ESP_initial - ESP_final) * (depth / 30)
        """
        esp_diff = max(0.0, current_esp_pct - target_esp_pct)
        gr_tons_ha = 0.086 * cec_meq_100g * esp_diff * (soil_depth_cm / 30.0)

        return {
            "initial_esp_pct": current_esp_pct,
            "target_esp_pct": target_esp_pct,
            "gypsum_requirement_tons_ha": round(gr_tons_ha, 2),
            "elemental_sulfur_equivalent_tons_ha": round(gr_tons_ha * 0.19, 2),
            "recommendation": "Incorporate gypsum evenly into topsoil and apply heavy leaching irrigation."
        }
