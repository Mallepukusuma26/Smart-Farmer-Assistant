"""
Revised Universal Soil Loss Equation (RUSLE) Engine.
Calculates annual soil erosion loss (A = R * K * LS * C * P) in metric tons/ha/year.
"""

from typing import Dict, Any

class SoilErosionRUSLEEngine:
    """RUSLE soil loss estimation calculator."""

    def calculate_annual_soil_loss(
        self,
        rainfall_erosivity_r: float,
        soil_erodibility_k: float,
        slope_length_steepness_ls: float,
        cover_management_c: float,
        support_practice_p: float
    ) -> Dict[str, float]:
        """
        A = R * K * LS * C * P
        """
        annual_loss_tons_ha = rainfall_erosivity_r * soil_erodibility_k * slope_length_steepness_ls * cover_management_c * support_practice_p

        # Soil loss tolerance threshold T ~ 10-12 tons/ha/yr
        t_tolerance = 11.2
        excessive = annual_loss_tons_ha > t_tolerance

        return {
            "r_factor": rainfall_erosivity_r,
            "k_factor": soil_erodibility_k,
            "ls_factor": slope_length_steepness_ls,
            "c_factor": cover_management_c,
            "p_factor": support_practice_p,
            "annual_soil_loss_tons_ha_yr": round(annual_loss_tons_ha, 2),
            "soil_tolerance_t_limit": t_tolerance,
            "erosion_risk_category": "Severe" if annual_loss_tons_ha > 25 else ("Moderate" if annual_loss_tons_ha > 11 else "Slight"),
            "exceeds_tolerance": excessive
        }
