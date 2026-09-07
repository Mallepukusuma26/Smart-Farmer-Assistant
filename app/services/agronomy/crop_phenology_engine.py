"""
Crop Phenology & Growing Degree Day (GDD) Accumulator Engine.
Calculates thermal time, phenological stage transitions, and maturity predictions.
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class CropThermalRequirement:
    crop_name: str
    t_base_c: float
    t_opt_c: float
    t_max_c: float
    gdd_emergence: float
    gdd_vegetative: float
    gdd_flowering: float
    gdd_maturity: float

class CropPhenologyEngine:
    """Thermal time and phenology prediction engine."""

    DEFAULT_CROP_PROFILES = {
        "wheat": CropThermalRequirement("Wheat", 4.0, 22.0, 35.0, 100.0, 500.0, 1000.0, 1600.0),
        "rice": CropThermalRequirement("Rice", 10.0, 30.0, 40.0, 120.0, 700.0, 1300.0, 2100.0),
        "maize": CropThermalRequirement("Maize", 10.0, 30.0, 44.0, 110.0, 650.0, 1200.0, 1850.0),
        "cotton": CropThermalRequirement("Cotton", 15.0, 32.0, 45.0, 150.0, 800.0, 1500.0, 2400.0),
        "sugarcane": CropThermalRequirement("Sugarcane", 12.0, 34.0, 45.0, 200.0, 1200.0, 2200.0, 3400.0),
    }

    def calculate_daily_gdd(self, temp_min: float, temp_max: float, t_base: float, t_max_cutoff: float) -> float:
        """Calculate single-day GDD using standard modified sine or cutoff method."""
        t_min_adj = max(t_base, min(temp_min, t_max_cutoff))
        t_max_adj = max(t_base, min(temp_max, t_max_cutoff))
        t_avg = (t_min_adj + t_max_adj) / 2.0
        return max(0.0, t_avg - t_base)

    def predict_phenology_stage(
        self, crop_name: str, daily_temperatures: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Track cumulative GDD from daily temp records [{'min': 15.0, 'max': 30.0}, ...]
        Returns current stage, GDD accumulated, and estimated days to maturity.
        """
        crop_key = crop_name.lower().strip()
        profile = self.DEFAULT_CROP_PROFILES.get(crop_key, self.DEFAULT_CROP_PROFILES["maize"])

        accumulated_gdd = 0.0
        days_elapsed = len(daily_temperatures)

        for temp in daily_temperatures:
            gdd = self.calculate_daily_gdd(temp['min'], temp['max'], profile.t_base_c, profile.t_max_c)
            accumulated_gdd += gdd

        if accumulated_gdd < profile.gdd_emergence:
            stage = "Germination / Emergence"
            completion_pct = (accumulated_gdd / profile.gdd_emergence) * 100.0
        elif accumulated_gdd < profile.gdd_vegetative:
            stage = "Vegetative Growth"
            completion_pct = (accumulated_gdd / profile.gdd_vegetative) * 100.0
        elif accumulated_gdd < profile.gdd_flowering:
            stage = "Flowering / Reproduction"
            completion_pct = (accumulated_gdd / profile.gdd_flowering) * 100.0
        elif accumulated_gdd < profile.gdd_maturity:
            stage = "Grain Filling / Ripening"
            completion_pct = (accumulated_gdd / profile.gdd_maturity) * 100.0
        else:
            stage = "Harvest Maturity"
            completion_pct = 100.0

        avg_gdd_per_day = accumulated_gdd / max(1, days_elapsed)
        remaining_gdd = max(0.0, profile.gdd_maturity - accumulated_gdd)
        est_days_to_harvest = remaining_gdd / max(1.0, avg_gdd_per_day)

        return {
            "crop_name": profile.crop_name,
            "accumulated_gdd": round(accumulated_gdd, 1),
            "target_maturity_gdd": profile.gdd_maturity,
            "current_stage": stage,
            "overall_maturity_pct": round(min(100.0, (accumulated_gdd / profile.gdd_maturity) * 100.0), 1),
            "days_elapsed": days_elapsed,
            "estimated_days_to_maturity": round(est_days_to_harvest, 1)
        }
