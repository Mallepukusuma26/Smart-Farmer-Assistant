"""
Agronomic Analytics & Field Yield Benchmarking Service.
Aggregates regional yield statistics, historical climate impacts, and agronomic performance indices.
"""

from typing import Dict, List, Any

class AgronomicAnalyticsService:
    """Regional yield benchmarking and multi-factor field performance service."""

    def benchmark_field_yield(self, field_id: int, actual_yield_tons_ha: float, crop_name: str) -> Dict[str, Any]:
        """Benchmark field yield against regional averages and potential water-limited yield."""
        regional_averages = {
            "wheat": 3.8,
            "rice": 4.5,
            "maize": 6.2,
            "cotton": 2.1,
            "sugarcane": 75.0
        }
        avg_yield = regional_averages.get(crop_name.lower(), 4.0)
        potential_yield = avg_yield * 1.45

        performance_index = (actual_yield_tons_ha / avg_yield) * 100.0
        yield_gap_tons_ha = max(0.0, potential_yield - actual_yield_tons_ha)

        return {
            "field_id": field_id,
            "crop_name": crop_name,
            "actual_yield_tons_ha": actual_yield_tons_ha,
            "regional_average_yield_tons_ha": avg_yield,
            "water_limited_potential_yield_tons_ha": potential_yield,
            "performance_index_pct": round(performance_index, 1),
            "yield_gap_tons_ha": round(yield_gap_tons_ha, 2),
            "yield_rating": "Superior" if performance_index >= 120 else ("Average" if performance_index >= 90 else "Underperforming")
        }
