"""
Agronomy Field Trafficability Engine for Smart Farmer Assistant.

Assesses soil moisture and bearing capacity for machinery field operations.
"""
from typing import Dict, Any

class AgronomyFieldTrafficabilityEngine:
    @staticmethod
    def assess_trafficability(soil_moisture_pct: float, field_capacity_pct: float, clay_pct: float) -> Dict[str, Any]:
        relative_moisture = soil_moisture_pct / max(1.0, field_capacity_pct)
        trafficable = True
        risk_level = 'Low'
        if relative_moisture > 0.95:
            trafficable = False
            risk_level = 'Severe Rutting and Compaction Risk'
        elif relative_moisture > 0.85:
            trafficable = True
            risk_level = 'Moderate Compaction Risk'
        return {
            'soil_moisture_pct': soil_moisture_pct,
            'field_capacity_pct': field_capacity_pct,
            'relative_moisture': round(relative_moisture, 2),
            'trafficable': trafficable,
            'compaction_risk': risk_level,
            'recommendation': 'Proceed with field machinery' if trafficable and relative_moisture <= 0.85 else 'Delay heavy field operations to avoid subsoil compaction'
        }
