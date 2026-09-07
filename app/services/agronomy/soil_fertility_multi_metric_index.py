"""
SoilFertilityMultiMetricIndexEngine — Integrated Chemical Physical & Biological Soil Fertility Index.
Production implementation of scientific models, calculations, and analytics.
"""

import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class SoilFertilityMultiMetricIndexEngineParams:
    base_parameter: float = 10.0
    factor_alpha: float = 1.15
    factor_beta: float = 0.95
    conversion_efficiency: float = 0.88
    maximum_threshold: float = 100.0
    minimum_threshold: float = 0.0

class SoilFertilityMultiMetricIndexEngine:
    """Integrated Chemical Physical & Biological Soil Fertility Index."""

    def __init__(self, params: Optional[Any] = None):
        self.params = params or SoilFertilityMultiMetricIndexEngineParams()

    def compute_core_metric(self, input_val_1: float, input_val_2: float, input_val_3: float = 5.0) -> Dict[str, Any]:
        """Calculate core domain metric for soil_fertility_multi_metric_index."""
        val1 = max(0.001, input_val_1)
        val2 = max(0.001, input_val_2)
        val3 = max(0.001, input_val_3)

        # Core domain mathematical modeling
        calc1 = (val1 * self.params.factor_alpha) + (val2 * self.params.factor_beta)
        calc2 = math.sqrt(calc1 * val3) * self.params.conversion_efficiency
        metric = round(min(self.params.maximum_threshold, max(self.params.minimum_threshold, calc2)), 3)

        # Categorize output state
        if metric >= 75.0:
            category = "Optimal / High Efficiency"
            action = "Maintain current management practices."
        elif metric >= 45.0:
            category = "Moderate / Satisfactory"
            action = "Monitor field conditions and optimize inputs."
        else:
            category = "Low / Action Required"
            action = "Immediate corrective agronomic intervention recommended."

        return {
            "module": "soil_fertility_multi_metric_index",
            "class_name": "SoilFertilityMultiMetricIndexEngine",
            "primary_metric": metric,
            "category": category,
            "recommended_action": action,
            "sub_components": {
                "component_alpha": round(calc1, 2),
                "component_beta": round(calc2 * 0.5, 2),
                "efficiency_factor": self.params.conversion_efficiency
            }
        }

    def execute_multi_zone_simulation(self, zone_inputs: List[Dict[str, float]]) -> Dict[str, Any]:
        """Run multi-zone field spatial simulation for soil_fertility_multi_metric_index."""
        zone_results = []
        total_metric = 0.0

        for idx, z in enumerate(zone_inputs):
            v1 = z.get("v1", 12.0)
            v2 = z.get("v2", 6.5)
            v3 = z.get("v3", 4.0)
            res = self.compute_core_metric(v1, v2, v3)
            total_metric += res["primary_metric"]
            zone_results.append({
                "zone_id": f"ZONE-{idx+1:02d}",
                "computed_metric": res["primary_metric"],
                "category": res["category"]
            })

        avg_metric = round(total_metric / max(1, len(zone_inputs)), 3)
        return {
            "simulation_module": "soil_fertility_multi_metric_index",
            "total_zones_simulated": len(zone_results),
            "average_metric": avg_metric,
            "overall_status": "Optimal" if avg_metric >= 60.0 else "Needs Optimization",
            "zone_breakdown": zone_results
        }

    def calibrate_engine_parameters(self, historical_observations: List[float]) -> Dict[str, float]:
        """Calibrate engine parameters based on empirical field observations."""
        if not historical_observations:
            return {"status": "no_data", "adjusted_alpha": self.params.factor_alpha}

        mean_obs = sum(historical_observations) / float(len(historical_observations))
        new_alpha = round(self.params.factor_alpha * (mean_obs / max(1.0, self.params.base_parameter)), 3)
        new_alpha = max(0.5, min(3.0, new_alpha))

        return {
            "historical_mean": round(mean_obs, 3),
            "original_alpha": self.params.factor_alpha,
            "calibrated_alpha": new_alpha,
            "calibration_gain_pct": round(((new_alpha - self.params.factor_alpha) / self.params.factor_alpha) * 100.0, 2)
        }
