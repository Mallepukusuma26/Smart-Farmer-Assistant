"""
Agronomy Crop Canopy Light Extinction K Engine for Smart Farmer Assistant.

Models Beer-Lambert extinction coefficient K for horizontal vs erectophile crop canopy architectures.
"""

import math
from typing import Dict, Any


class AgronomyCropCanopyLightExtinctionEngine:
    """Calculates extinction coefficient K and solar radiation transmission fraction through crop canopy."""

    @staticmethod
    def calculate_canopy_k_factor(
        crop_leaf_angle_deg: float = 60.0,
        solar_zenith_angle_deg: float = 30.0,
        leaf_area_index: float = 3.5
    ) -> Dict[str, Any]:
        """
        Extinction K = sqrt(x^2 + tan^2(theta)) / (x + 1.774 * (x + 1.182)^-0.733)
        """
        rad_zenith = math.radians(solar_zenith_angle_deg)
        # Approximate K for typical crop geometry (erectophile vs planophile)
        if crop_leaf_angle_deg > 65.0:
            k = round(max(0.35, 0.4 + 0.2 * math.cos(rad_zenith)), 3)
            architecture = "Erectophile (Vertical Leaf Canopy — e.g. Maize/Wheat)"
        elif crop_leaf_angle_deg < 40.0:
            k = round(min(0.95, 0.75 + 0.15 * math.cos(rad_zenith)), 3)
            architecture = "Planophile (Horizontal Leaf Canopy — e.g. Soybean/Cotton)"
        else:
            k = 0.60
            architecture = "Spherical / Intermediate Canopy Architecture"

        transmissivity = round(math.exp(-k * leaf_area_index), 4)

        return {
            "leaf_angle_degrees": crop_leaf_angle_deg,
            "solar_zenith_angle_deg": solar_zenith_angle_deg,
            "calculated_extinction_k": k,
            "canopy_architecture_class": architecture,
            "radiation_transmission_fraction": transmissivity,
            "light_interception_pct": round((1.0 - transmissivity) * 100.0, 1)
        }
