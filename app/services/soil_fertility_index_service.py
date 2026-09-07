"""
Soil Fertility Index Service Module for Smart Farmer Assistant.

Calculates multi-parameter Soil Quality Index (SQI), micronutrient availability models
(Zinc, Iron, Copper, Manganese, Boron), and CEC cation exchange capacity calculations.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class SoilFertilityIndexService:
    """
    Business service providing multi-parameter Soil Quality Index (SQI),
    micronutrient sufficiency evaluation, and base saturation calculations.
    """

    @staticmethod
    def evaluate_micronutrients(
        zn_ppm: float,
        fe_ppm: float,
        cu_ppm: float,
        mn_ppm: float,
        b_ppm: float
    ) -> Dict[str, Any]:
        """
        Evaluates DTPA-extractable soil micronutrients against critical threshold limits.
        """
        evaluations = {
            "zinc_zn": {"value_ppm": zn_ppm, "status": "Deficient" if zn_ppm < 0.6 else "Sufficient"},
            "iron_fe": {"value_ppm": fe_ppm, "status": "Deficient" if fe_ppm < 4.5 else "Sufficient"},
            "copper_cu": {"value_ppm": cu_ppm, "status": "Deficient" if cu_ppm < 0.2 else "Sufficient"},
            "manganese_mn": {"value_ppm": mn_ppm, "status": "Deficient" if mn_ppm < 2.0 else "Sufficient"},
            "boron_b": {"value_ppm": b_ppm, "status": "Deficient" if b_ppm < 0.5 else "Sufficient"}
        }

        deficient_count = sum(1 for v in evaluations.values() if v["status"] == "Deficient")

        return {
            "micronutrients": evaluations,
            "deficient_elements_count": deficient_count,
            "overall_status": "Balanced Micronutrients" if deficient_count == 0 else f"{deficient_count} Micronutrients Deficient",
            "foliar_recommendation": "Foliar spray of Zinc Sulfate (0.5%) + Ferrous Sulfate (0.5%) recommended" if deficient_count > 0 else "No micronutrient foliar spray required"
        }

    @staticmethod
    def calculate_cation_exchange_capacity(
        ca_meq: float,
        mg_meq: float,
        k_meq: float,
        na_meq: float,
        h_meq: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculates Cation Exchange Capacity (CEC meq/100g) and Base Saturation percentage.
        CEC = Ca + Mg + K + Na + H
        """
        cec = ca_meq + mg_meq + k_meq + na_meq + h_meq
        bases = ca_meq + mg_meq + k_meq + na_meq
        base_sat_pct = (bases / cec) * 100.0 if cec > 0 else 0.0

        ca_sat_pct = (ca_meq / cec) * 100.0 if cec > 0 else 0.0
        mg_sat_pct = (mg_meq / cec) * 100.0 if cec > 0 else 0.0
        k_sat_pct = (k_meq / cec) * 100.0 if cec > 0 else 0.0

        return {
            "cec_meq_100g": round(cec, 2),
            "base_saturation_pct": round(base_sat_pct, 2),
            "calcium_saturation_pct": round(ca_sat_pct, 2),
            "magnesium_saturation_pct": round(mg_sat_pct, 2),
            "potassium_saturation_pct": round(k_sat_pct, 2),
            "ca_mg_ratio": round(ca_meq / mg_meq, 2) if mg_meq > 0 else 0.0,
            "balance_rating": "Ideal Cation Balance (65% Ca, 15% Mg, 5% K)" if 60 <= ca_sat_pct <= 75 else "Imbalanced Cation Saturation"
        }
