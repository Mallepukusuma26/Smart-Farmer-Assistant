"""
Grain Drying & Post-Harvest Storage Service Module for Smart Farmer Assistant.

Calculates Equilibrium Moisture Content (EMC) using modified Henderson equation,
heated air psychrometrics, grain drying aeration runtime, and energy cost math.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class GrainDryingService:
    """
    Business service calculating Equilibrium Moisture Content (EMC %) using modified Henderson model,
    ambient air drying psychrometrics, and drying energy requirements.
    """

    @staticmethod
    def calculate_modified_henderson_emc(
        temperature_c: float,
        relative_humidity_pct: float,
        grain_type: str = "rice"
    ) -> Dict[str, Any]:
        """
        Calculates Equilibrium Moisture Content (EMC % dry basis) using Modified Henderson Equation:
        1 - RH = exp(-K * (T + C) * M_e^N)
        """
        rh = min(max(relative_humidity_pct / 100.0, 0.05), 0.95)
        temp_k = temperature_c + 273.15

        # Henderson constants for grain species
        # K, C, N constants
        grain_constants = {
            "rice": {"K": 0.0000191, "C": 51.16, "N": 2.44},
            "wheat": {"K": 0.0000257, "C": 70.0, "N": 2.21},
            "corn": {"K": 0.0000865, "C": 49.81, "N": 1.86},
            "soybean": {"K": 0.0003053, "C": 134.0, "N": 1.22}
        }

        consts = grain_constants.get(grain_type.lower().strip(), grain_constants["rice"])
        k_val = consts["K"]
        c_val = consts["C"]
        n_val = consts["N"]

        # Solve for M_e (EMC)
        try:
            emc_db = math.pow(-math.log(1.0 - rh) / (k_val * (temperature_c + c_val)), 1.0 / n_val)
            emc_wb = (emc_db / (100.0 + emc_db)) * 100.0 if emc_db > 0 else 12.0
        except (ValueError, ZeroDivisionError):
            emc_wb = 13.5

        emc_wb = round(max(min(emc_wb, 30.0), 5.0), 2)

        return {
            "grain_type": grain_type,
            "ambient_temperature_c": temperature_c,
            "relative_humidity_pct": relative_humidity_pct,
            "equilibrium_moisture_content_emc_pct": emc_wb,
            "safe_storage_moisture_pct": 14.0,
            "storage_suitability": "Safe for Storage" if emc_wb <= 14.0 else "High Mold Risk — Mechanical Drying Required"
        }
