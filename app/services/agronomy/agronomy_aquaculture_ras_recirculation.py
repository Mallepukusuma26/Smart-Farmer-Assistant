"""
Agronomy Aquaculture RAS Recirculation Engine for Smart Farmer Assistant.

Models Recirculating Aquaculture System (RAS) Total Ammonia Nitrogen (TAN), biofilter sizing, and dissolved oxygen (DO) saturation.
"""

from typing import Dict, Any


class AgronomyAquacultureRASEngine:
    """Calculates aquaculture biofilter nitrifying surface area (m2), TAN production, and oxygenation rate."""

    @staticmethod
    def calculate_ras_biofilter_size(
        daily_feed_input_kg: float,
        feed_protein_pct: float = 32.0,
        water_temp_c: float = 26.0,
        target_tan_ppm: float = 1.0
    ) -> Dict[str, Any]:
        """
        TAN production = Daily Feed (kg) * Protein % * 0.092 (16% N * 57.5% excreted as TAN)
        Nitrification Rate (VTR) = 0.45 g TAN/m2/day of biofilter media surface
        """
        tan_production_g_day = round(daily_feed_input_kg * (feed_protein_pct / 100.0) * 92.0, 1)
        required_biofilter_surface_m2 = round(tan_production_g_day / 0.45, 1)

        # Assuming biofilter media specific surface area SSA = 600 m2/m3
        biofilter_media_volume_m3 = round(required_biofilter_surface_m2 / 600.0, 2)
        daily_oxygen_demand_kg = round(daily_feed_input_kg * 0.25 + (tan_production_g_day * 0.00457), 2)

        return {
            "daily_feed_input_kg": daily_feed_input_kg,
            "feed_protein_pct": feed_protein_pct,
            "daily_tan_generated_g": tan_production_g_day,
            "required_biofilter_media_surface_m2": required_biofilter_surface_m2,
            "required_biofilter_media_volume_m3": biofilter_media_volume_m3,
            "daily_dissolved_oxygen_demand_kg": daily_oxygen_demand_kg,
            "water_turnover_recommendation": f"Recirculate water through biofilter at least 2.5 times per hour to keep TAN below {target_tan_ppm} ppm."
        }
