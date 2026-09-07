"""
Compliance Audit Service Module for Smart Farmer Assistant.

Manages agricultural compliance checks, pesticide Pre-Harvest Interval (PHI) safety audits,
groundwater nitrate contamination risk evaluation, and GAP (Good Agricultural Practices) standards.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ComplianceAuditService:
    """
    Business service executing Good Agricultural Practices (GAP) safety audits,
    groundwater leaching risk scoring, and chemical pesticide buffer zone checks.
    """

    @staticmethod
    def audit_nitrate_leaching_risk(
        applied_nitrogen_kg_acre: float,
        crop_n_uptake_kg_acre: float,
        irrigation_over_application_pct: float = 10.0,
        soil_sand_pct: float = 40.0
    ) -> Dict[str, Any]:
        """
        Evaluates potential nitrate (NO3-N) leaching into groundwater reserves.
        """
        excess_n = max(applied_nitrogen_kg_acre - crop_n_uptake_kg_acre, 0.0)
        leaching_factor = (soil_sand_pct / 100.0) * (1.0 + (irrigation_over_application_pct / 100.0))
        potential_leached_n_kg = excess_n * leaching_factor

        if potential_leached_n_kg > 20.0:
            risk = "HIGH RISK — Potential Groundwater Contamination"
            advice = "Split Nitrogen applications, use slow-release Urea, or plant deep-rooted cover crops."
        elif potential_leached_n_kg > 10.0:
            risk = "MODERATE RISK"
            advice = "Match Nitrogen application timing strictly with crop uptake demand curves."
        else:
            risk = "LOW RISK — Environmentally Compliant"
            advice = "Nitrogen management meets Good Agricultural Practices (GAP) standards."

        return {
            "applied_nitrogen_kg_acre": applied_nitrogen_kg_acre,
            "crop_n_uptake_kg_acre": crop_n_uptake_kg_acre,
            "excess_nitrogen_kg_acre": round(excess_n, 2),
            "potential_leached_n_kg_acre": round(potential_leached_n_kg, 2),
            "nitrate_leaching_risk": risk,
            "gap_advice": advice
        }
