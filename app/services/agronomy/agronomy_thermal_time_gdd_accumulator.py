"""
Agronomy Thermal Time Growing Degree Days (GDD) Accumulator Engine for Smart Farmer Assistant.

Calculates accumulated growing degree days for phenological stage transitions.
"""
from typing import List, Dict, Any

class AgronomyThermalTimeGDDAccumulatorEngine:
    @staticmethod
    def accumulate_gdd(daily_tmax: List[float], daily_tmin: List[float], t_base: float = 10.0, t_cutoff: float = 30.0) -> Dict[str, Any]:
        total_gdd = 0.0
        daily_records = []
        for tmax, tmin in zip(daily_tmax, daily_tmin):
            adj_max = min(t_cutoff, tmax)
            adj_min = max(t_base, tmin)
            t_avg = (adj_max + adj_min) / 2.0
            gdd = max(0.0, t_avg - t_base)
            total_gdd += gdd
            daily_records.append(round(gdd, 1))
        return {
            'days_count': len(daily_tmax),
            't_base': t_base,
            't_cutoff': t_cutoff,
            'total_accumulated_gdd': round(total_gdd, 1),
            'daily_gdd_series': daily_records
        }
