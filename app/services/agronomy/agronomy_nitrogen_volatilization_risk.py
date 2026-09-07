"""
Agronomy Nitrogen Volatilization Risk Engine for Smart Farmer Assistant.

Calculates ammonia volatilization from surface-applied urea under high pH and wind.
"""
from typing import Dict, Any

class AgronomyNitrogenVolatilizationRiskEngine:
    @staticmethod
    def assess_volatilization(surface_applied_urea_kg_ha: float, soil_ph: float, temp_c: float, wind_speed_m_s: float) -> Dict[str, Any]:
        risk_score = 0.0
        if soil_ph > 7.0:
            risk_score += (soil_ph - 7.0) * 20.0
        if temp_c > 25.0:
            risk_score += (temp_c - 25.0) * 1.5
        risk_score += wind_speed_m_s * 5.0
        loss_pct = min(45.0, max(2.0, risk_score * 0.5))
        loss_kg_n_ha = round(surface_applied_urea_kg_ha * 0.46 * (loss_pct / 100.0), 2)
        return {
            'applied_urea_kg_ha': surface_applied_urea_kg_ha,
            'soil_ph': soil_ph,
            'estimated_n_loss_pct': round(loss_pct, 1),
            'estimated_nh3_loss_kg_n_ha': loss_kg_n_ha,
            'mitigation_recommendation': 'Incorporate urea into top 5cm soil immediately or use urease inhibitor' if loss_pct > 15.0 else 'Low volatilization risk'
        }
