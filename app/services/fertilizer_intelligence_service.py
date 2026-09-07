"""
Fertilizer Intelligence Service Module for Smart Farmer Assistant.

Provides NPK nutrient deficit calculations, fertilizer blending, application stage scheduling,
inventory tracking, cost analytics, and agronomic safety recommendations.
"""

from typing import Dict, Any, List, Optional
from app.repositories.fertilizer_repository import FertilizerRepository


class FertilizerIntelligenceService:
    """
    Fertilizer Intelligence engine for N-P-K nutrient deficit calculation,
    fertilizer dosage optimization, split application scheduling, and cost estimation.
    """

    def __init__(self, repository: Optional[FertilizerRepository] = None):
        self.repository = repository or FertilizerRepository()

    def calculate_npk_deficit_and_dosage(
        self,
        current_n: float,
        current_p: float,
        current_k: float,
        target_crop: str = "Wheat",
        area_acres: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculates exact N-P-K nutrient deficits and computes commercial fertilizer requirements
        (Urea, Single Super Phosphate, Muriate of Potash, DAP) per acre.
        """
        # Crop recommended NPK targets in kg/acre
        crop_targets = {
            "Wheat": {"N": 50.0, "P": 25.0, "K": 20.0},
            "Rice": {"N": 60.0, "P": 30.0, "K": 30.0},
            "Maize": {"N": 55.0, "P": 25.0, "K": 25.0},
            "Cotton": {"N": 45.0, "P": 20.0, "K": 20.0},
            "Sugarcane": {"N": 100.0, "P": 40.0, "K": 50.0},
            "Potato": {"N": 70.0, "P": 45.0, "K": 60.0}
        }

        target = crop_targets.get(target_crop, {"N": 50.0, "P": 25.0, "K": 20.0})

        # Calculate net nutrient deficit per acre (assuming soil test is in kg/acre equivalent)
        n_deficit = max(0.0, target["N"] - (current_n * 0.2))
        p_deficit = max(0.0, target["P"] - (current_p * 0.3))
        k_deficit = max(0.0, target["K"] - (current_k * 0.25))

        # Commercial fertilizer conversions
        # Urea = 46% N
        # SSP = 16% P2O5
        # MOP = 60% K2O
        # DAP = 18% N, 46% P2O5
        urea_kg = round((n_deficit / 0.46) * area_acres, 1)
        ssp_kg = round((p_deficit / 0.16) * area_acres, 1)
        mop_kg = round((k_deficit / 0.60) * area_acres, 1)

        # Estimated fertilizer cost (INR prices per kg)
        est_cost = (urea_kg * 6.0) + (ssp_kg * 8.0) + (mop_kg * 34.0)

        return {
            "target_crop": target_crop,
            "area_acres": area_acres,
            "target_npk_kg_per_acre": target,
            "net_nutrient_deficit_kg": {
                "N": round(n_deficit * area_acres, 1),
                "P": round(p_deficit * area_acres, 1),
                "K": round(k_deficit * area_acres, 1)
            },
            "commercial_fertilizer_schedule": [
                {"fertilizer": "Urea (46% N)", "total_bag_count_50kg": round(urea_kg / 50.0, 1), "total_kg": urea_kg, "est_cost_inr": round(urea_kg * 6.0, 2)},
                {"fertilizer": "Single Super Phosphate (16% P2O5)", "total_bag_count_50kg": round(ssp_kg / 50.0, 1), "total_kg": ssp_kg, "est_cost_inr": round(ssp_kg * 8.0, 2)},
                {"fertilizer": "Muriate of Potash (60% K2O)", "total_bag_count_50kg": round(mop_kg / 50.0, 1), "total_kg": mop_kg, "est_cost_inr": round(mop_kg * 34.0, 2)}
            ],
            "total_fertilizer_cost_inr": round(est_cost, 2),
            "split_application_advice": [
                "Basal Dose (At Sowing): Apply 100% SSP, 100% MOP, and 25% Urea.",
                "First Top Dressing (30 Days After Sowing): Apply 50% Urea.",
                "Second Top Dressing (60 Days After Sowing / Flowering): Apply remaining 25% Urea."
            ]
        }
