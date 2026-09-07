"""
Agronomy Aquaponics Nitrification & TAN Engine for Smart Farmer Assistant.

Models fish waste Total Ammonia Nitrogen (TAN), Nitrosomonas/Nitrobacter conversion rates, and plant N uptake.
"""

from typing import Dict, Any


class AgronomyAquaponicsNitrificationEngine:
    """Calculates aquaponic fish-to-plant ratio, nitrate production (NO3-N ppm), and pH buffering."""

    @staticmethod
    def calculate_aquaponic_tan_balance(
        fish_biomass_kg: float,
        daily_feed_rate_pct: float = 1.5,
        plant_bed_area_m2: float = 20.0
    ) -> Dict[str, Any]:
        """
        Daily Feed (g) = Biomass * Feed %
        TAN (g) = Feed (g) * 0.03
        Nitrate NO3-N Produced (g) = TAN (g) * 4.43
        """
        daily_feed_g = fish_biomass_kg * 10.0 * daily_feed_rate_pct
        tan_g_day = round(daily_feed_g * 0.03, 1)
        nitrate_g_day = round(tan_g_day * 4.43, 1)

        # Plant uptake capacity ~ 0.5 - 0.8 g NO3-N / m2 / day
        plant_uptake_capacity_g = plant_bed_area_m2 * 0.65
        balance = round(nitrate_g_day - plant_uptake_capacity_g, 1)

        system_status = "Balanced Nitrogen System" if abs(balance) < 5.0 else (
            "High Nitrate Accumulation — Increase Plant Density or Harvest Fish" if balance > 5.0 else "Low Nitrate — Increase Fish Feeding Rate"
        )

        return {
            "fish_biomass_kg": fish_biomass_kg,
            "daily_feed_input_g": daily_feed_g,
            "daily_tan_production_g": tan_g_day,
            "daily_nitrate_generated_g": nitrate_g_day,
            "plant_bed_area_m2": plant_bed_area_m2,
            "plant_nitrate_uptake_capacity_g": round(plant_uptake_capacity_g, 1),
            "net_nitrogen_balance_g_day": balance,
            "system_health_status": system_status
        }
