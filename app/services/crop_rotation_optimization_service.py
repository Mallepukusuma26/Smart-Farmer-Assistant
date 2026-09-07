"""
Crop Rotation Optimization Service Module for Smart Farmer Assistant.

Models multi-year crop succession, legume nitrogen fixation credits, and weed/pest suppression cycles.
"""

from typing import Dict, Any, List


class CropRotationOptimizationService:
    """Optimizes multi-season crop rotation sequences to maximize soil N accumulation and break pest life-cycles."""

    def evaluate_rotation_compatibility(self, current_crop: str, proposed_crop: str) -> Dict[str, Any]:
        """Calculates agronomic compatibility score (0-100) between consecutive crop seasons."""
        c1 = current_crop.lower()
        c2 = proposed_crop.lower()

        score = 80.0
        nitrogen_credit_kg_ha = 0.0

        legumes = ["chickpea", "gram", "groundnut", "soybean", "lentils", "pulses", "peas"]
        cereals = ["wheat", "rice", "paddy", "maize", "barley", "sorghum"]
        solanaceous = ["potato", "tomato", "eggplant", "chilli"]

        if c1 == c2:
            score = 30.0
            notes = "High Risk: Monoculture cropping leads to severe root pathogen accumulation."
        elif any(leg in c1 for leg in legumes) and any(cer in c2 for cer in cereals):
            score = 95.0
            nitrogen_credit_kg_ha = 40.0
            notes = "Optimal Rotation: Legume-cereal rotation fixes biological nitrogen and enhances cereal yield."
        elif any(sol in c1 for sol in solanaceous) and any(sol in c2 for sol in solanaceous):
            score = 40.0
            notes = "Incompatible: Consecutive solanaceous crops promote bacterial wilt and nematode infestation."
        else:
            score = 75.0
            notes = "Acceptable crop rotation sequence."

        return {
            "current_crop": current_crop,
            "proposed_crop": proposed_crop,
            "compatibility_score": score,
            "rotation_rating": "Highly Recommended" if score >= 85.0 else ("Acceptable" if score >= 65.0 else "Not Recommended"),
            "estimated_nitrogen_credit_kg_ha": nitrogen_credit_kg_ha,
            "agronomic_recommendation": notes
        }
