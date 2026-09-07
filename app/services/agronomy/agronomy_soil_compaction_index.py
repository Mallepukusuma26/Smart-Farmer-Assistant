"""
Agronomy Soil Compaction Index Engine for Smart Farmer Assistant.

Evaluates soil bulk density and penetrometer resistance to assess root growth restriction risks.
"""
from typing import Dict, Any

class AgronomySoilCompactionIndexEngine:
    @staticmethod
    def assess_compaction(bulk_density_g_cm3: float, soil_texture: str, cone_penetrometer_psi: float) -> Dict[str, Any]:
        critical_density = 1.65 if 'clay' in soil_texture.lower() else 1.80
        compaction_risk = 'Low'
        if bulk_density_g_cm3 >= critical_density or cone_penetrometer_psi > 300:
            compaction_risk = 'High'
        elif bulk_density_g_cm3 >= (critical_density - 0.15) or cone_penetrometer_psi > 200:
            compaction_risk = 'Moderate'
        return {
            'bulk_density_g_cm3': bulk_density_g_cm3,
            'critical_density_threshold': critical_density,
            'penetrometer_psi': cone_penetrometer_psi,
            'compaction_risk_level': compaction_risk,
            'recommendation': 'Subsoiling / deep tillage required' if compaction_risk == 'High' else 'Standard tillage practices'
        }
