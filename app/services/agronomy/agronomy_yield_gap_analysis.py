"""
Agronomy Yield Gap Analysis Engine for Smart Farmer Assistant.

Computes potential yield, water-limited yield, and actual yield gaps for crops.
"""
from typing import Dict, Any

class AgronomyYieldGapAnalysisEngine:
    @staticmethod
    def analyze_yield_gap(potential_yield_t_ha: float, actual_yield_t_ha: float) -> Dict[str, Any]:
        yield_gap_t_ha = round(potential_yield_t_ha - actual_yield_t_ha, 2)
        exploitation_rate_pct = round((actual_yield_t_ha / max(0.1, potential_yield_t_ha)) * 100, 1)
        return {
            'potential_yield_t_ha': potential_yield_t_ha,
            'actual_yield_t_ha': actual_yield_t_ha,
            'yield_gap_t_ha': yield_gap_t_ha,
            'exploitation_rate_pct': exploitation_rate_pct,
            'closing_gap_priority': 'High' if exploitation_rate_pct < 70 else 'Medium' if exploitation_rate_pct < 85 else 'Low'
        }
