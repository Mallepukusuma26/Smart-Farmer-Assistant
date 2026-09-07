"""
Agronomy Drought Susceptibility Index (DSI) Engine for Smart Farmer Assistant.

Quantifies crop yield stability under water deficit conditions.
"""
from typing import Dict, Any

class AgronomyDroughtSusceptibilityIndexEngine:
    @staticmethod
    def calculate_dsi(yield_stress: float, yield_potential: float, mean_yield_stress_all: float, mean_yield_potential_all: float) -> Dict[str, Any]:
        if yield_potential <= 0 or mean_yield_potential_all <= 0:
            return {'error': 'Invalid yield values for DSI calculation'}
        stress_intensity = 1.0 - (mean_yield_stress_all / mean_yield_potential_all)
        if stress_intensity <= 0:
            dsi = 0.0
        else:
            dsi = round((1.0 - (yield_stress / yield_potential)) / stress_intensity, 3)
        tolerance_category = 'Highly Tolerant' if dsi < 0.5 else 'Moderately Tolerant' if dsi <= 1.0 else 'Susceptible'
        return {
            'yield_stress': yield_stress,
            'yield_potential': yield_potential,
            'drought_susceptibility_index': dsi,
            'tolerance_category': tolerance_category
        }
