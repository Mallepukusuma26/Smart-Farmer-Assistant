"""
Fertilizer Recommendation Predictor Module for Smart Farmer Assistant.

Provides hybrid rule-based and ML-assisted fertilizer recommendation engine
calculating nitrogen, phosphorus, potassium deficiencies, dosage per acre/hectare,
and stage-wise application splitting schedules.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)


class FertilizerPredictor:
    """
    Hybrid offline recommendation engine combining agronomic crop nutrient target rules
    with soil laboratory test analysis.
    """

    def __init__(self):
        # Target crop nutrient requirements (kg/acre)
        self.crop_targets = {
            "rice": {"N": 40.0, "P": 20.0, "K": 20.0},
            "wheat": {"N": 45.0, "P": 22.0, "K": 18.0},
            "maize": {"N": 50.0, "P": 25.0, "K": 25.0},
            "corn": {"N": 50.0, "P": 25.0, "K": 25.0},
            "tomato": {"N": 60.0, "P": 30.0, "K": 35.0},
            "potato": {"N": 55.0, "P": 28.0, "K": 30.0},
            "cotton": {"N": 48.0, "P": 24.0, "K": 24.0},
            "soybean": {"N": 15.0, "P": 30.0, "K": 20.0},  # Low N due to nitrogen fixation
            "groundnut": {"N": 12.0, "P": 25.0, "K": 18.0},
            "sugarcane": {"N": 100.0, "P": 40.0, "K": 50.0}
        }

    def predict_fertilizer_requirement(
        self,
        crop_name: str,
        soil_n_mg_kg: float,
        soil_p_mg_kg: float,
        soil_k_mg_kg: float,
        area_acres: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculates NPK deficiencies, recommended fertilizer quantities (Urea, DAP, MOP),
        and application schedule split across Basal, Vegetative, and Flowering stages.
        """
        crop_lower = crop_name.lower().strip()
        target = self.crop_targets.get(crop_lower, {"N": 40.0, "P": 20.0, "K": 20.0})

        # Soil test nutrient status factor (mg/kg conversion factor ~ 0.2)
        avail_n_kg_acre = soil_n_mg_kg * 0.2
        avail_p_kg_acre = soil_p_mg_kg * 0.2
        avail_k_kg_acre = soil_k_mg_kg * 0.2

        def_n = max(target["N"] - avail_n_kg_acre, 0.0)
        def_p = max(target["P"] - avail_p_kg_acre, 0.0)
        def_k = max(target["K"] - avail_k_kg_acre, 0.0)

        # Commercial fertilizer math: DAP (18-46-0), Urea (46-0-0), MOP (0-0-60)
        dap_kg_acre = (def_p / 0.46) if def_p > 0 else 0.0
        n_from_dap = dap_kg_acre * 0.18
        rem_n = max(def_n - n_from_dap, 0.0)
        urea_kg_acre = (rem_n / 0.46) if rem_n > 0 else 0.0
        mop_kg_acre = (def_k / 0.60) if def_k > 0 else 0.0

        total_dap = dap_kg_acre * area_acres
        total_urea = urea_kg_acre * area_acres
        total_mop = mop_kg_acre * area_acres

        # Application split schedule
        schedule = [
            {
                "stage": "Basal Application (At Sowing / Planting)",
                "dap_kg": round(total_dap, 2),
                "urea_kg": round(total_urea * 0.33, 2),
                "mop_kg": round(total_mop * 0.50, 2),
                "instructions": "Incorporate into soil during seedbed preparation."
            },
            {
                "stage": "First Top Dressing (Vegetative Stage / 25-30 Days)",
                "dap_kg": 0.0,
                "urea_kg": round(total_urea * 0.33, 2),
                "mop_kg": 0.0,
                "instructions": "Broadcast Urea when soil is moist, follow with light irrigation."
            },
            {
                "stage": "Second Top Dressing (Panicle / Flowering Stage / 50-60 Days)",
                "dap_kg": 0.0,
                "urea_kg": round(total_urea * 0.34, 2),
                "mop_kg": round(total_mop * 0.50, 2),
                "instructions": "Apply Urea and remaining MOP prior to flowering."
            }
        ]

        return {
            "crop_name": crop_name,
            "area_acres": area_acres,
            "nutrient_deficiencies_kg_acre": {"N": round(def_n, 2), "P": round(def_p, 2), "K": round(def_k, 2)},
            "recommended_fertilizers_kg_acre": {
                "urea_kg_acre": round(urea_kg_acre, 2),
                "dap_kg_acre": round(dap_kg_acre, 2),
                "mop_kg_acre": round(mop_kg_acre, 2)
            },
            "total_fertilizer_required_kg": {
                "total_urea_kg": round(total_urea, 2),
                "total_dap_kg": round(total_dap, 2),
                "total_mop_kg": round(total_mop, 2)
            },
            "application_schedule": schedule
        }
