"""
Pest Population Degree-Day & Economic Threshold Engine.
Simulates insect pest life-cycle development (Degree-Days) and Economic Injury Level (EIL).
"""

from typing import Dict, Any

class PestPopulationDegreeDayEngine:
    """Insect pest physiological time and economic threshold calculator."""

    def calculate_economic_injury_level(
        self,
        control_cost_usd_ha: float,
        market_price_usd_ton: float,
        crop_yield_loss_per_pest_ton_ha: float,
        control_efficacy_pct: float = 85.0
    ) -> Dict[str, float]:
        """
        EIL = C / (V * I * D * K)
        Where:
          C = Cost of management per area ($/ha)
          V = Market value of crop ($/ton)
          I = Injury per pest density (loss/ha/pest)
          D = Damage per unit injury
          K = Proportionate reduction in pest population by control (0-1)
        """
        k_factor = max(0.1, min(1.0, control_efficacy_pct / 100.0))
        eil_pest_density = control_cost_usd_ha / (market_price_usd_ton * crop_yield_loss_per_pest_ton_ha * k_factor)
        economic_threshold = eil_pest_density * 0.75  # Action threshold at 75% of EIL

        return {
            "control_cost_usd_ha": control_cost_usd_ha,
            "market_price_usd_ton": market_price_usd_ton,
            "economic_injury_level_pests_m2": round(eil_pest_density, 2),
            "economic_threshold_action_trigger_m2": round(economic_threshold, 2),
            "recommendation": "Apply chemical/biological control if scouted pest density exceeds ET threshold."
        }
