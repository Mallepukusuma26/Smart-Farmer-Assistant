"""
Crop Phenology Service Module for Smart Farmer Assistant.

Manages BBCH phenological growth stage modeling (Germination, Leaf Development,
Tillering/Stem Elongation, Inflorescence, Flowering, Fruit Development, Ripening),
accumulated Thermal Time (GDD), and stage-specific agronomic management alerts.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class CropPhenologyService:
    """
    Business service mapping accumulated Growing Degree Days (GDD) to standard BBCH growth stages.
    """

    def __init__(self):
        self.bbch_stages = {
            "rice": [
                {"stage_code": "BBCH 00-09", "name": "Germination", "min_gdd": 0, "max_gdd": 100},
                {"stage_code": "BBCH 10-19", "name": "Leaf Development", "min_gdd": 101, "max_gdd": 300},
                {"stage_code": "BBCH 20-29", "name": "Tillering", "min_gdd": 301, "max_gdd": 600},
                {"stage_code": "BBCH 30-39", "name": "Stem Elongation", "min_gdd": 601, "max_gdd": 850},
                {"stage_code": "BBCH 50-59", "name": "Panicle Initiation", "min_gdd": 851, "max_gdd": 1100},
                {"stage_code": "BBCH 60-69", "name": "Flowering / Anthesis", "min_gdd": 1101, "max_gdd": 1350},
                {"stage_code": "BBCH 70-89", "name": "Milk & Dough Grain Ripening", "min_gdd": 1351, "max_gdd": 1700},
                {"stage_code": "BBCH 90-99", "name": "Harvest Maturity", "min_gdd": 1701, "max_gdd": 2200}
            ],
            "wheat": [
                {"stage_code": "BBCH 00-09", "name": "Germination", "min_gdd": 0, "max_gdd": 120},
                {"stage_code": "BBCH 10-19", "name": "Leaf Development", "min_gdd": 121, "max_gdd": 350},
                {"stage_code": "BBCH 20-29", "name": "Tillering", "min_gdd": 351, "max_gdd": 650},
                {"stage_code": "BBCH 30-39", "name": "Stem Extension", "min_gdd": 651, "max_gdd": 900},
                {"stage_code": "BBCH 50-59", "name": "Heading / Ear Emergence", "min_gdd": 901, "max_gdd": 1150},
                {"stage_code": "BBCH 60-69", "name": "Flowering", "min_gdd": 1151, "max_gdd": 1400},
                {"stage_code": "BBCH 70-89", "name": "Ripening / Grain Filling", "min_gdd": 1401, "max_gdd": 1800},
                {"stage_code": "BBCH 90-99", "name": "Maturity", "min_gdd": 1801, "max_gdd": 2100}
            ]
        }

    def predict_bbch_growth_stage(self, crop_name: str, accumulated_gdd: float) -> Dict[str, Any]:
        """
        Predicts current BBCH growth stage and remaining GDD until harvest maturity.
        """
        crop_lower = crop_name.lower().strip()
        stages = self.bbch_stages.get(crop_lower, self.bbch_stages["rice"])

        current_stage = stages[0]
        for st in stages:
            if st["min_gdd"] <= accumulated_gdd <= st["max_gdd"]:
                current_stage = st
                break
            elif accumulated_gdd > st["max_gdd"]:
                current_stage = st

        maturity_gdd = stages[-1]["max_gdd"]
        remaining_gdd = max(maturity_gdd - accumulated_gdd, 0.0)
        progress_pct = min((accumulated_gdd / maturity_gdd) * 100.0, 100.0)

        return {
            "crop_name": crop_name,
            "accumulated_gdd": accumulated_gdd,
            "current_bbch_stage_code": current_stage["stage_code"],
            "current_stage_name": current_stage["name"],
            "progress_to_maturity_pct": round(progress_pct, 1),
            "remaining_gdd_to_maturity": round(remaining_gdd, 1),
            "stage_agronomic_recommendation": f"Stage {current_stage['name']}: Ensure adequate soil moisture and monitor for stage-specific pests."
        }
