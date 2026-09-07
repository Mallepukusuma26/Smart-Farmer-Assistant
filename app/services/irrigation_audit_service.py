"""
Irrigation Audit Service Module for Smart Farmer Assistant.

Manages irrigation system efficiency audits, Christiansen Uniformity Coefficient (CU),
Distribution Uniformity (DU), emitter clogging evaluation, and friction head loss math.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class IrrigationAuditService:
    """
    Business service auditing drip and sprinkler irrigation performance,
    Christiansen Uniformity Coefficient (CU %), Distribution Uniformity (DU %),
    and Darcy-Weisbach / Hazen-Williams pipe friction head loss.
    """

    @staticmethod
    def calculate_christiansen_uniformity(catch_can_volumes_ml: List[float]) -> Dict[str, Any]:
        """
        Calculates Christiansen Uniformity Coefficient (CU %) for sprinkler/drip systems:
        CU = 100 * (1 - sum(|x_i - mean|) / (n * mean))
        """
        if not catch_can_volumes_ml:
            return {"cu_pct": 0.0, "rating": "Invalid Catch Can Data"}

        n = len(catch_can_volumes_ml)
        mean_vol = sum(catch_can_volumes_ml) / n
        if mean_vol <= 0:
            return {"cu_pct": 0.0, "rating": "Zero Flow Detected"}

        abs_deviations = sum(abs(v - mean_vol) for v in catch_can_volumes_ml)
        cu_pct = 100.0 * (1.0 - (abs_deviations / (n * mean_vol)))
        cu_pct = round(max(min(cu_pct, 100.0), 0.0), 2)

        # Distribution Uniformity (DU %) = Low Quarter Mean / Overall Mean
        sorted_vols = sorted(catch_can_volumes_ml)
        low_quarter_count = max(1, math.floor(n / 4))
        low_quarter_mean = sum(sorted_vols[:low_quarter_count]) / low_quarter_count
        du_pct = round((low_quarter_mean / mean_vol) * 100.0, 2)

        if cu_pct >= 85.0:
            rating = "Excellent Uniformity"
        elif cu_pct >= 75.0:
            rating = "Good Uniformity"
        elif cu_pct >= 65.0:
            rating = "Fair Uniformity — Maintenance Recommended"
        else:
            rating = "Poor Uniformity — Check Emitter Clogging & Pressure"

        return {
            "num_catch_cans": n,
            "mean_catch_volume_ml": round(mean_vol, 2),
            "christiansen_uniformity_cu_pct": cu_pct,
            "distribution_uniformity_du_pct": du_pct,
            "uniformity_rating": rating
        }

    @staticmethod
    def calculate_hazen_williams_friction_loss(
        flow_rate_lpm: float,
        pipe_length_m: float,
        inner_diameter_mm: float,
        c_factor: float = 140.0
    ) -> Dict[str, Any]:
        """
        Calculates Hazen-Williams pipe friction head loss in meters of water column.
        h_f = 10.67 * L * Q^1.852 / (C^1.852 * D^4.87)
        """
        if inner_diameter_mm <= 0 or flow_rate_lpm <= 0:
            return {"friction_head_loss_m": 0.0, "pressure_drop_bar": 0.0}

        # Convert units: Q in m3/s, D in m
        q_m3s = flow_rate_lpm / 60000.0
        d_m = inner_diameter_mm / 1000.0

        hf_m = (10.67 * pipe_length_m * math.pow(q_m3s, 1.852)) / (math.pow(c_factor, 1.852) * math.pow(d_m, 4.87))
        pressure_drop_bar = hf_m * 0.0980665

        return {
            "flow_rate_lpm": flow_rate_lpm,
            "pipe_length_m": pipe_length_m,
            "inner_diameter_mm": inner_diameter_mm,
            "hazen_williams_c_factor": c_factor,
            "friction_head_loss_m": round(hf_m, 2),
            "pressure_drop_bar": round(pressure_drop_bar, 3),
            "recommendation": "Acceptable pressure loss" if pressure_drop_bar <= 0.5 else "Excessive friction drop — consider larger pipe diameter."
        }
