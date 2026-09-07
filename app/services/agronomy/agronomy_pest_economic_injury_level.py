"""
Agronomy Pest Economic Injury Level (EIL) Engine for Smart Farmer Assistant.

Computes Economic Threshold (ET) and Economic Injury Level (EIL) for pest control decision support.
"""

from typing import Dict, Any


class AgronomyPestEconomicInjuryLevelEngine:
    """Calculates pest population thresholds for spraying economic feasibility."""

    @staticmethod
    def calculate_eil_and_action_threshold(
        control_cost_per_acre_inr: float,
        market_price_per_quintal_inr: float,
        yield_loss_per_pest_quintal: float,
        control_efficiency_pct: float = 85.0
    ) -> Dict[str, Any]:
        """
        EIL = C / (V * I * D * K)
        C = Cost of management per area
        V = Market value per unit yield
        I = Injury per pest density
        D = Damage per unit injury
        K = Proportionate reduction in pest population
        """
        k = max(0.5, control_efficiency_pct / 100.0)
        v = market_price_per_quintal_inr
        d = yield_loss_per_pest_quintal

        if (v * d * k) <= 0:
            return {"error": "Invalid market price or yield loss values."}

        eil_pest_count = round(control_cost_per_acre_inr / (v * d * k), 2)
        # Action threshold (ET) is typically 75% of EIL
        economic_threshold_count = round(eil_pest_count * 0.75, 2)

        return {
            "control_cost_per_acre_inr": control_cost_per_acre_inr,
            "market_price_per_quintal_inr": market_price_per_quintal_inr,
            "economic_injury_level_pests_per_plant": eil_pest_count,
            "economic_action_threshold_pests_per_plant": economic_threshold_count,
            "spray_decision_rule": f"Initiate treatment when pest count exceeds {economic_threshold_count} pests per plant."
        }
