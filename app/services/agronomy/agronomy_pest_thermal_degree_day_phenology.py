"""
Agronomy Pest Thermal Degree-Day Phenology Engine for Smart Farmer Assistant.

Models thermal degree-day (GDD) accumulation for insect pest population generation cycles and spray windows.
"""

from typing import Dict, Any, List


class AgronomyPestThermalDegreeDayEngine:
    """Calculates cumulative degree-days for insect pest emergence (Helicoverpa, Spodoptera, Stem Borer)."""

    @staticmethod
    def calculate_pest_gdd_emergence(
        daily_max_temps_c: List[float],
        daily_min_temps_c: List[float],
        pest_base_temp_c: float = 10.0,
        generation_gdd_target: float = 450.0
    ) -> Dict[str, Any]:
        """
        Daily GDD = max(0, ((T_max + T_min) / 2) - T_base)
        """
        accumulated_gdd = 0.0
        days_count = len(daily_max_temps_c)

        for i in range(days_count):
            t_max = daily_max_temps_c[i]
            t_min = daily_min_temps_c[i]
            t_avg = (t_max + t_min) / 2.0
            gdd = max(0.0, t_avg - pest_base_temp_c)
            accumulated_gdd += gdd

        accumulated_gdd = round(accumulated_gdd, 1)
        completion_pct = round(min(100.0, (accumulated_gdd / generation_gdd_target) * 100.0), 1)

        emerged_generation = int(accumulated_gdd / generation_gdd_target)
        next_gen_gdd_remaining = round(generation_gdd_target - (accumulated_gdd % generation_gdd_target), 1)

        spray_window_alert = "CRITICAL SPRAY WINDOW: Egg hatch / 1st instar larvae peak expected now!" if (accumulated_gdd % generation_gdd_target) >= (generation_gdd_target * 0.85) else "Regular Pheromone Trap Monitoring"

        return {
            "monitored_days_count": days_count,
            "pest_base_temperature_c": pest_base_temp_c,
            "cumulative_gdd_accumulated": accumulated_gdd,
            "pest_generations_completed": emerged_generation,
            "current_generation_progress_pct": completion_pct,
            "gdd_remaining_for_next_egg_hatch": next_gen_gdd_remaining,
            "action_warning": spray_window_alert
        }
