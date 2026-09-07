"""
Crop-Weed Competition Yield Loss Engine.
Implements Cousens hyperbolic crop-weed competition equation and
Critical Period for Weed Control (CPWC) models.
"""

import math
from typing import Dict, Any

class WeedCompetitionEngine:
    """Cousens hyperbolic model for estimating crop yield loss due to weed density."""

    def calculate_yield_loss_cousens(
        self, weed_density_plants_m2: float, parameter_i: float = 0.8, parameter_a: float = 85.0
    ) -> Dict[str, float]:
        """
        Cousens Model: Y_loss (%) = (I * d) / (1 + (I * d / A))
        Where:
          d = weed density (plants/m2)
          I = yield loss per unit weed density as d -> 0
          A = maximum asymptotic yield loss (%) as d -> infinity
        """
        d = weed_density_plants_m2
        if d <= 0:
            return {"yield_loss_pct": 0.0, "retained_yield_pct": 100.0}

        y_loss = (parameter_i * d) / (1.0 + (parameter_i * d / max(1.0, parameter_a)))
        y_loss = min(parameter_a, max(0.0, y_loss))

        return {
            "weed_density_m2": d,
            "yield_loss_pct": round(y_loss, 2),
            "retained_yield_pct": round(100.0 - y_loss, 2),
            "action_threshold_exceeded": d > 5.0
        }
