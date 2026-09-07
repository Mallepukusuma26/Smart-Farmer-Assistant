"""
1D Soil Hydrodynamics & van Genuchten Water Retention Engine.
Calculates unsaturated soil matric potential h, volumetric water content theta,
and unsaturated hydraulic conductivity K(h).
"""

import math
from typing import Dict, Any

class SoilHydrodynamicsRichardsEngine:
    """van Genuchten (1980) soil water retention kinetics calculator."""

    def calculate_van_genuchten_retention(
        self,
        matric_potential_cm: float,
        theta_r: float = 0.045,  # Residual water content
        theta_s: float = 0.43,   # Saturated water content
        alpha: float = 0.015,    # Inverse of air-entry value
        n_param: float = 1.41,   # Pore-size distribution index
        ks_cm_day: float = 24.5  # Saturated hydraulic conductivity
    ) -> Dict[str, float]:
        """
        Theta(h) = Theta_r + (Theta_s - Theta_r) / [1 + (|alpha * h|)^n]^m
        Where m = 1 - 1/n
        """
        h = abs(matric_potential_cm)
        m = 1.0 - (1.0 / max(1.01, n_param))

        denominator = (1.0 + (alpha * h) ** n_param) ** m
        theta_h = theta_r + (theta_s - theta_r) / max(0.001, denominator)

        # Effective saturation Se
        se = (theta_h - theta_r) / max(0.001, (theta_s - theta_r))
        se = max(0.001, min(1.0, se))

        # Mualem-van Genuchten hydraulic conductivity K(Se)
        k_h = ks_cm_day * (se ** 0.5) * ((1.0 - (1.0 - (se ** (1.0 / m))) ** m) ** 2)

        return {
            "matric_potential_cm": matric_potential_cm,
            "volumetric_water_content": round(theta_h, 3),
            "volumetric_water_content_pct": round(theta_h * 100.0, 1),
            "effective_saturation_se": round(se, 3),
            "hydraulic_conductivity_cm_day": round(k_h, 4)
        }
