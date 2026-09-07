"""
Agronomic Modeling Service Module for Smart Farmer Assistant.

Provides integrated crop yield response, thermal unit tracking, and regional climate adaptation modeling.
"""

from typing import Dict, Any, List, Optional
import math


class AgronomicModelingService:
    """Integrated agronomic modeling engine for multi-factor yield and climate adaptation."""

    def calculate_integrated_yield_potential(
        self,
        base_yield_tons: float,
        nitrogen_kg_ha: float,
        irrigation_coverage_pct: float,
        soil_health_score: float,
        pest_damage_pct: float = 0.0
    ) -> Dict[str, Any]:
        """
        Multi-variable multiplicative yield potential model:
        Yield = Base * (N_Factor * Irrigation_Factor * Soil_Factor) * (1 - Pest_Loss)
        """
        n_factor = min(1.3, max(0.6, 0.6 + (nitrogen_kg_ha / 180.0) * 0.5))
        irr_factor = min(1.25, max(0.7, 0.7 + (irrigation_coverage_pct / 100.0) * 0.45))
        soil_factor = min(1.2, max(0.5, soil_health_score / 85.0))
        pest_factor = max(0.2, 1.0 - (pest_damage_pct / 100.0))

        potential_yield_tons = round(base_yield_tons * n_factor * irr_factor * soil_factor * pest_factor, 2)
        yield_gap_tons = round(max(0.0, (base_yield_tons * 1.35) - potential_yield_tons), 2)

        return {
            "base_yield_tons": base_yield_tons,
            "calculated_yield_potential_tons": potential_yield_tons,
            "yield_gap_tons": yield_gap_tons,
            "nitrogen_response_factor": round(n_factor, 2),
            "irrigation_response_factor": round(irr_factor, 2),
            "soil_health_factor": round(soil_factor, 2),
            "pest_loss_factor": round(pest_factor, 2),
            "limiting_factor_analysis": "Nitrogen Supply" if n_factor < min(irr_factor, soil_factor) else (
                "Irrigation Water" if irr_factor < soil_factor else "Soil Health & Organic Matter"
            )
        }
