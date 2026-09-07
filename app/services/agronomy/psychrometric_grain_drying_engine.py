"""
Grain Drying Psychrometrics & Equilibrium Moisture Content (EMC) Engine.
Implements Modified Chung-Pfost equations for EMC and grain drying aeration times.
"""

import math
from typing import Dict, Any

class PsychrometricGrainDryingEngine:
    """Grain drying EMC kinetics and air drying calculations."""

    # Modified Chung-Pfost parameters (A, B, C) for crops
    CHUNG_PFOST_PARAMS = {
        "wheat": {"A": 0.356, "B": 0.211, "C": 12.3},
        "maize": {"A": 0.312, "B": 0.254, "C": 14.2},
        "paddy": {"A": 0.421, "B": 0.185, "C": 10.8},
        "soybean": {"A": 0.298, "B": 0.310, "C": 15.6}
    }

    def calculate_emc(self, temp_c: float, relative_humidity_pct: float, crop: str = "wheat") -> float:
        """Calculate Equilibrium Moisture Content (% dry basis) using Modified Chung-Pfost equation."""
        crop_key = crop.lower().strip()
        params = self.CHUNG_PFOST_PARAMS.get(crop_key, self.CHUNG_PFOST_PARAMS["wheat"])
        
        rh = max(0.05, min(0.99, relative_humidity_pct / 100.0))
        t_k = temp_c + 273.15

        try:
            emc_db = (-1.0 / params["B"]) * math.log(-((t_k - params["C"]) * math.log(rh)) / params["A"])
            emc_wb = (emc_db / (100.0 + emc_db)) * 100.0
            return round(max(5.0, min(35.0, emc_wb)), 2)
        except Exception:
            return 13.5

    def calculate_drying_time_hours(
        self, initial_mc_wb: float, target_mc_wb: float, grain_mass_tons: float, airflow_m3_min_ton: float = 2.0
    ) -> Dict[str, float]:
        """Estimate hours needed for in-bin ambient air grain drying."""
        mc_diff_pct = max(0.0, initial_mc_wb - target_mc_wb)
        water_to_remove_kg = grain_mass_tons * 1000.0 * (mc_diff_pct / 100.0)

        # Average water removal rate ~0.15 kg water per m3 air airflow
        water_removal_rate_kg_hr = airflow_m3_min_ton * grain_mass_tons * 60.0 * 0.005
        drying_hours = water_to_remove_kg / max(0.1, water_removal_rate_kg_hr)

        return {
            "initial_moisture_pct": initial_mc_wb,
            "target_moisture_pct": target_mc_wb,
            "water_to_remove_kg": round(water_to_remove_kg, 1),
            "estimated_drying_hours": round(drying_hours, 1),
            "estimated_drying_days": round(drying_hours / 24.0, 1)
        }
