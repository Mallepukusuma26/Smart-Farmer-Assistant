"""
Agronomic Features Module for Smart Farmer Assistant.

Computes agricultural domain feature indexes:
1. Growing Degree Days (GDD)
2. Soil Water Deficit Index (SWDI)
3. NPK Nutrient Balance Ratio
4. Crop Heat Units (CHU)
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class AgronomicFeatureEngine:
    """
    Feature engineering module calculating agricultural agronomic indexes.
    """

    @staticmethod
    def calculate_gdd(t_max_c: float, t_min_c: float, t_base_c: float = 10.0) -> float:
        """
        Calculates Growing Degree Days (GDD = (T_max + T_min)/2 - T_base).
        """
        t_mean = (t_max_c + t_min_c) / 2.0
        gdd = max(t_mean - t_base_c, 0.0)
        return round(gdd, 2)

    @staticmethod
    def calculate_npk_ratio(n: float, p: float, k: float) -> Dict[str, float]:
        """
        Computes N:P:K nutrient ratios normalized to Phosphorus = 1.
        """
        if p <= 0:
            return {"n_ratio": round(n, 2), "p_ratio": 1.0, "k_ratio": round(k, 2)}
        return {
            "n_ratio": round(n / p, 2),
            "p_ratio": 1.0,
            "k_ratio": round(k / p, 2)
        }

    @staticmethod
    def calculate_swdi(field_capacity_pct: float, wilting_point_pct: float, current_moisture_pct: float) -> float:
        """
        Calculates Soil Water Deficit Index (SWDI).
        SWDI = 10 * (theta - theta_fc) / (theta_fc - theta_wp)
        """
        denom = field_capacity_pct - wilting_point_pct
        if denom <= 0:
            return 0.0
        swdi = 10.0 * (current_moisture_pct - field_capacity_pct) / denom
        return round(max(min(swdi, 10.0), -10.0), 2)
