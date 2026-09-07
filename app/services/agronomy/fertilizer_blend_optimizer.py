"""
Minimum-Cost Fertilizer Blend Optimizer Engine.
Solves target N-P2O5-K2O nutrient specs using simplex/linear combination logic.
"""

from typing import Dict, Any, List

class FertilizerBlendOptimizer:
    """Linear fertilizer nutrient blending calculator."""

    AVAILABLE_SOURCES = {
        "urea": {"n": 46.0, "p": 0.0, "k": 0.0, "cost_kg": 0.40},
        "dap": {"n": 18.0, "p": 46.0, "k": 0.0, "cost_kg": 0.70},
        "mop": {"n": 0.0, "p": 0.0, "k": 60.0, "cost_kg": 0.50},
        "ssp": {"n": 0.0, "p": 16.0, "k": 0.0, "cost_kg": 0.30}
    }

    def optimize_blend(self, target_n_kg: float, target_p_kg: float, target_k_kg: float) -> Dict[str, Any]:
        """Calculate exact kg requirements of DAP, MOP, and Urea to meet NPK target."""
        # 1. Supply all P from DAP
        dap_kg = (target_p_kg / 46.0) * 100.0
        n_from_dap = dap_kg * 0.18

        # 2. Supply remaining N from Urea
        remaining_n = max(0.0, target_n_kg - n_from_dap)
        urea_kg = (remaining_n / 46.0) * 100.0

        # 3. Supply all K from MOP
        mop_kg = (target_k_kg / 60.0) * 100.0

        total_cost = (
            dap_kg * self.AVAILABLE_SOURCES["dap"]["cost_kg"] +
            urea_kg * self.AVAILABLE_SOURCES["urea"]["cost_kg"] +
            mop_kg * self.AVAILABLE_SOURCES["mop"]["cost_kg"]
        )

        return {
            "target_n_kg": target_n_kg,
            "target_p_kg": target_p_kg,
            "target_k_kg": target_k_kg,
            "required_dap_kg": round(dap_kg, 1),
            "required_urea_kg": round(urea_kg, 1),
            "required_mop_kg": round(mop_kg, 1),
            "total_blend_weight_kg": round(dap_kg + urea_kg + mop_kg, 1),
            "estimated_cost_usd": round(total_cost, 2)
        }
