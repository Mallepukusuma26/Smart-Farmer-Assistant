"""
Agronomy Crop Water Productivity (CWP) Engine for Smart Farmer Assistant.

Calculates yield per unit of evapotranspired water (kg/m3).
"""
from typing import Dict, Any

class AgronomyCropWaterProductivityEngine:
    @staticmethod
    def calculate_cwp(yield_kg_ha: float, total_evapotranspiration_mm: float) -> Dict[str, Any]:
        water_volume_m3 = total_evapotranspiration_mm * 10.0
        if water_volume_m3 <= 0:
            cwp_kg_m3 = 0.0
        else:
            cwp_kg_m3 = round(yield_kg_ha / water_volume_m3, 3)
        return {
            'yield_kg_ha': yield_kg_ha,
            'evapotranspiration_mm': total_evapotranspiration_mm,
            'water_volume_m3_ha': water_volume_m3,
            'crop_water_productivity_kg_m3': cwp_kg_m3,
            'benchmarking': 'High Efficiency' if cwp_kg_m3 >= 1.5 else 'Average Efficiency' if cwp_kg_m3 >= 0.8 else 'Needs Improvement'
        }
