"""
Agronomy Pesticide Half-Life Degradation Engine for Smart Farmer Assistant.

Models first-order chemical degradation kinetics, pre-harvest interval (PHI) compliance, and residue safety bounds.
"""

import math
from typing import Dict, Any


class AgronomyPesticideDegradationEngine:
    """Calculates chemical residue dissipation half-life (DT50) and pre-harvest interval (PHI) days."""

    @staticmethod
    def calculate_pesticide_residue_dissipation(
        initial_dose_ppm: float,
        dt50_half_life_days: float,
        application_days_ago: float,
        mrl_threshold_ppm: float = 0.05
    ) -> Dict[str, Any]:
        """
        C(t) = C0 * exp(-k * t)
        k = ln(2) / DT50
        """
        k = math.log(2) / max(0.5, dt50_half_life_days)
        current_residue_ppm = round(initial_dose_ppm * math.exp(-k * application_days_ago), 4)

        # Days required to reach MRL (Maximum Residue Limit)
        if initial_dose_ppm > mrl_threshold_ppm:
            days_to_mrl = math.ceil(math.log(initial_dose_ppm / mrl_threshold_ppm) / k)
        else:
            days_to_mrl = 0

        safe_to_harvest = current_residue_ppm <= mrl_threshold_ppm
        remaining_phi_days = max(0, days_to_mrl - int(application_days_ago))

        return {
            "initial_dose_ppm": initial_dose_ppm,
            "half_life_dt50_days": dt50_half_life_days,
            "days_since_application": application_days_ago,
            "current_residue_ppm": current_residue_ppm,
            "mrl_threshold_ppm": mrl_threshold_ppm,
            "safe_for_harvest": safe_to_harvest,
            "required_phi_days_total": days_to_mrl,
            "remaining_waiting_period_days": remaining_phi_days,
            "harvest_guidance": "Crop meets food safety Maximum Residue Limit (MRL) standards." if safe_to_harvest else f"DO NOT HARVEST — Wait {remaining_phi_days} additional days for pesticide residue dissipation."
        }
