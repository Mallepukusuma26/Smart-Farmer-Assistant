"""
Agronomy Precision Seed Rate Calculator Engine for Smart Farmer Assistant.

Computes exact seed sowing rate (kg/acre), plant population density, germination adjustments, and seed cost.
"""

from typing import Dict, Any


class AgronomyPrecisionSeedRateEngine:
    """Calculates precision seed rate based on 1000-grain weight (test weight), germination %, and field purity."""

    @staticmethod
    def calculate_precision_seed_rate(
        target_plant_population_per_acre: float,
        thousand_grain_weight_g: float,
        germination_pct: float = 85.0,
        purity_pct: float = 98.0,
        field_survival_pct: float = 90.0,
        seed_cost_per_kg_inr: float = 85.0
    ) -> Dict[str, Any]:
        """
        Pure Live Seed (PLS) = Germination % * Purity %
        Seed Rate (kg/acre) = (Target Population * 1000-Grain Weight (g)) / (PLS * Field Survival * 100,000)
        """
        pls_fraction = (germination_pct / 100.0) * (purity_pct / 100.0)
        survival_fraction = field_survival_pct / 100.0

        if pls_fraction <= 0 or survival_fraction <= 0:
            return {"error": "Germination, purity, and survival percentages must be greater than zero."}

        # Weight in kg per grain = (thousand_grain_weight_g / 1000) / 1000
        total_seeds_needed = target_plant_population_per_acre / (pls_fraction * survival_fraction)
        seed_rate_kg_acre = round((total_seeds_needed * thousand_grain_weight_g) / 1000000.0, 2)
        total_seed_cost_inr = round(seed_rate_kg_acre * seed_cost_per_kg_inr, 2)

        return {
            "target_plant_population_per_acre": target_plant_population_per_acre,
            "thousand_grain_weight_g": thousand_grain_weight_g,
            "pure_live_seed_pls_pct": round(pls_fraction * 100.0, 2),
            "calculated_seed_rate_kg_per_acre": seed_rate_kg_acre,
            "total_seed_cost_per_acre_inr": total_seed_cost_inr,
            "sowing_adjustment_note": f"Adjust seeder rate to apply {seed_rate_kg_acre} kg/acre to account for {germination_pct}% germination and {purity_pct}% purity."
        }
