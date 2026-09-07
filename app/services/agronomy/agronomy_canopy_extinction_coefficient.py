"""
Agronomy Canopy Light Extinction Coefficient Engine for Smart Farmer Assistant.

Calculates PAR attenuation through the crop canopy using Beer-Lambert law.
"""
import math
from typing import Dict, Any

class AgronomyCanopyExtinctionCoefficientEngine:
    @staticmethod
    def calculate_par_interception(leaf_area_index: float, extinction_k: float = 0.65, incident_par_mj_m2: float = 20.0) -> Dict[str, Any]:
        interception_fraction = 1.0 - math.exp(-extinction_k * leaf_area_index)
        intercepted_par = round(incident_par_mj_m2 * interception_fraction, 2)
        transmitted_par = round(incident_par_mj_m2 - intercepted_par, 2)
        return {
            'leaf_area_index': leaf_area_index,
            'extinction_k': extinction_k,
            'interception_fraction_pct': round(interception_fraction * 100, 1),
            'intercepted_par_mj_m2': intercepted_par,
            'transmitted_par_mj_m2': transmitted_par
        }
