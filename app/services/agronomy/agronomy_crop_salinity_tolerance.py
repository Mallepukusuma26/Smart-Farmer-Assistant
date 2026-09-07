"""
Agronomy Crop Salinity Tolerance Engine for Smart Farmer Assistant.

Models Maas-Hoffman yield reduction function based on electrical conductivity (ECe).
"""
from typing import Dict, Any

class AgronomyCropSalinityToleranceEngine:
    @staticmethod
    def calculate_yield_reduction(ece_ds_m: float, threshold_ece: float = 1.7, slope_pct_per_ds_m: float = 12.0) -> Dict[str, Any]:
        if ece_ds_m <= threshold_ece:
            yield_loss_pct = 0.0
        else:
            yield_loss_pct = min(100.0, round((ece_ds_m - threshold_ece) * slope_pct_per_ds_m, 1))
        expected_yield_pct = round(100.0 - yield_loss_pct, 1)
        return {
            'ece_ds_m': ece_ds_m,
            'threshold_ece': threshold_ece,
            'yield_loss_pct': yield_loss_pct,
            'expected_yield_pct': expected_yield_pct,
            'salinity_hazard': 'Severe' if yield_loss_pct > 30 else 'Moderate' if yield_loss_pct > 10 else 'None'
        }
