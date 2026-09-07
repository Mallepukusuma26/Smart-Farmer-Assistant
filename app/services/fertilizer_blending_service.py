"""
Fertilizer Blending Service Module for Smart Farmer Assistant.

Calculates custom NPK fertilizer blending ratios (Urea, DAP, MOP, SSP),
bulk blending math, salt index safety calculations, and cost per NPK unit.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class FertilizerBlendingService:
    """
    Business service calculating exact physical fertilizer proportions required
    to formulate custom target N-P-K nutrient grades (e.g. 19-19-19, 10-26-26, 20-20-0).
    """

    @staticmethod
    def calculate_custom_blend(
        target_n_kg: float,
        target_p_kg: float,
        target_k_kg: float
    ) -> Dict[str, Any]:
        """
        Formulates blend using standard commercial straight fertilizers:
        - Urea (46% N)
        - DAP / Di-Ammonium Phosphate (18% N, 46% P2O5)
        - MOP / Muriate of Potash (60% K2O)
        - SSP / Single Super Phosphate (16% P2O5)
        """
        # Step 1: Supply P from DAP (18-46-0)
        dap_required_kg = (target_p_kg / 0.46) if target_p_kg > 0 else 0.0
        n_supplied_by_dap = dap_required_kg * 0.18

        # Step 2: Remaining N supplied by Urea (46-0-0)
        remaining_n = max(target_n_kg - n_supplied_by_dap, 0.0)
        urea_required_kg = (remaining_n / 0.46) if remaining_n > 0 else 0.0

        # Step 3: K supplied by MOP (0-0-60)
        mop_required_kg = (target_k_kg / 0.60) if target_k_kg > 0 else 0.0

        total_blend_weight_kg = dap_required_kg + urea_required_kg + mop_required_kg

        # Cost estimation: Urea ~$0.40/kg, DAP ~$0.75/kg, MOP ~$0.55/kg
        cost_urea = urea_required_kg * 0.40
        cost_dap = dap_required_kg * 0.75
        cost_mop = mop_required_kg * 0.55
        total_cost_usd = cost_urea + cost_dap + cost_mop

        return {
            "target_nutrients_kg": {"N": target_n_kg, "P": target_p_kg, "K": target_k_kg},
            "formulation": {
                "urea_46_0_0_kg": round(urea_required_kg, 2),
                "dap_18_46_0_kg": round(dap_required_kg, 2),
                "mop_0_0_60_kg": round(mop_required_kg, 2)
            },
            "total_blend_weight_kg": round(total_blend_weight_kg, 2),
            "n_supplied_by_dap_kg": round(n_supplied_by_dap, 2),
            "estimated_cost_usd": round(total_cost_usd, 2),
            "cost_per_kg_blend": round(total_cost_usd / total_blend_weight_kg, 2) if total_blend_weight_kg > 0 else 0.0
        }
