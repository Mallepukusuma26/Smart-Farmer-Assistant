"""
Agronomy Grain Drying Equilibrium Moisture Content (EMC) Engine for Smart Farmer Assistant.

Models Modified Henderson / Chung-Pfost equilibrium moisture content (EMC %) for safe grain storage.
"""

import math
from typing import Dict, Any


class AgronomyGrainDryingEMCEngine:
    """Calculates Equilibrium Moisture Content (EMC %) for wheat, corn, rice, and soybean in ambient storage air."""

    @staticmethod
    def calculate_emc(
        grain_type: str,
        air_temp_c: float,
        relative_humidity_pct: float
    ) -> Dict[str, Any]:
        """
        Modified Henderson Equation for EMC:
        EMC = [-ln(1 - RH) / (K * (T + C))] ^ (1 / N)
        """
        rh_frac = min(0.99, max(0.05, relative_humidity_pct / 100.0))
        temp_k = air_temp_c + 273.15

        # Crop specific constants for Henderson equation
        emc_table = {
            "Wheat": {"K": 0.00011, "N": 2.28},
            "Corn": {"K": 0.00008, "N": 2.30},
            "Rice": {"K": 0.00014, "N": 2.10},
            "Soybean": {"K": 0.00035, "N": 1.75}
        }

        consts = emc_table.get(grain_type, {"K": 0.00011, "N": 2.28})
        k = consts["K"]
        n = consts["N"]

        emc_val = ((-math.log(1.0 - rh_frac)) / (k * temp_k)) ** (1.0 / n)
        emc_pct = round(max(5.0, min(25.0, emc_val)), 2)

        safe_storage_limit = 12.0 if grain_type == "Soybean" else 13.5
        is_safe = emc_pct <= safe_storage_limit

        return {
            "grain_type": grain_type,
            "air_temperature_c": air_temp_c,
            "relative_humidity_pct": relative_humidity_pct,
            "equilibrium_moisture_content_emc_pct": emc_pct,
            "safe_storage_moisture_limit_pct": safe_storage_limit,
            "storage_safety_status": "Safe for Long-term Storage" if is_safe else "High Mold Risk — Grain Drying Required Before Storage",
            "drying_guidance": f"Air at {air_temp_c}°C & {relative_humidity_pct}% RH will dry grain to {emc_pct}% final equilibrium moisture."
        }
