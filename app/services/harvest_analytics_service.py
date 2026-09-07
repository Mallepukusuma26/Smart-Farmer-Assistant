"""
Harvest Analytics Service Module for Smart Farmer Assistant.

Manages harvest yield logging, grain moisture shrinkage math, combine harvester loss,
storage warehouse capacity tracking, and post-harvest loss estimation.
"""

from typing import Dict, Any, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


class HarvestAnalyticsService:
    """
    Business service calculating grain moisture shrinkage discount, post-harvest losses,
    and storage warehouse capacity utilization.
    """

    @staticmethod
    def calculate_moisture_shrinkage(
        initial_weight_kg: float,
        initial_moisture_pct: float,
        target_moisture_pct: float = 14.0
    ) -> Dict[str, Any]:
        """
        Calculates grain weight loss due to drying from initial moisture % down to target market moisture %.
        Final Weight = Initial Weight * (100 - Initial Moisture) / (100 - Target Moisture)
        """
        if initial_moisture_pct <= target_moisture_pct:
            return {
                "initial_weight_kg": initial_weight_kg,
                "initial_moisture_pct": initial_moisture_pct,
                "target_moisture_pct": target_moisture_pct,
                "final_weight_after_drying_kg": initial_weight_kg,
                "shrinkage_weight_loss_kg": 0.0,
                "shrinkage_pct": 0.0
            }

        final_weight = initial_weight_kg * (100.0 - initial_moisture_pct) / (100.0 - target_moisture_pct)
        weight_loss = initial_weight_kg - final_weight
        shrinkage_pct = (weight_loss / initial_weight_kg) * 100.0

        return {
            "initial_weight_kg": round(initial_weight_kg, 2),
            "initial_moisture_pct": initial_moisture_pct,
            "target_moisture_pct": target_moisture_pct,
            "final_weight_after_drying_kg": round(final_weight, 2),
            "shrinkage_weight_loss_kg": round(weight_loss, 2),
            "shrinkage_pct": round(shrinkage_pct, 2)
        }

    @staticmethod
    def estimate_harvester_combine_loss(
        header_loss_kg_acre: float,
        cylinder_loss_kg_acre: float,
        separation_loss_kg_acre: float,
        area_acres: float
    ) -> Dict[str, Any]:
        """
        Calculates total mechanical combine harvest loss across header, threshing, and cleaning.
        """
        total_loss_per_acre = header_loss_kg_acre + cylinder_loss_kg_acre + separation_loss_kg_acre
        total_field_loss = total_loss_per_acre * area_acres

        return {
            "header_loss_kg_acre": header_loss_kg_acre,
            "cylinder_loss_kg_acre": cylinder_loss_kg_acre,
            "separation_loss_kg_acre": separation_loss_kg_acre,
            "total_combine_loss_kg_acre": round(total_loss_per_acre, 2),
            "total_harvest_loss_kg": round(total_field_loss, 2),
            "estimated_financial_loss_usd": round((total_field_loss / 1000.0) * 450.0, 2),
            "recommendation": "Adjust combine ground speed and reel height if total loss exceeds 20 kg/acre."
        }
