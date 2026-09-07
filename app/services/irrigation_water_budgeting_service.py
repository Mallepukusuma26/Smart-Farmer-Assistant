"""
Irrigation Water Budgeting Service Module for Smart Farmer Assistant.

Models seasonal farm-wide water allocation, reservoir depletion rates, and irrigation pumping efficiency.
"""

from typing import Dict, Any, List, Optional


class IrrigationWaterBudgetingService:
    """Computes farm seasonal water balance, groundwater recharge estimates, and irrigation allocation."""

    def calculate_seasonal_water_balance(
        self,
        farm_area_acres: float,
        seasonal_rainfall_mm: float,
        planned_crops: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Total Water Input = (Rainfall mm * 4.04686 * Area)
        Total Water Demand = Sum(Crop Area * Crop Water Req m3)
        Net Deficit = Demand - (Rainfall * Effective Efficiency)
        """
        rainfall_volume_m3 = round(seasonal_rainfall_mm * 4.04686 * farm_area_acres, 1)
        effective_rain_m3 = round(rainfall_volume_m3 * 0.65, 1)

        total_demand_m3 = 0.0
        crop_summary = []

        for crop in planned_crops:
            area = float(crop.get("acres", 1.0))
            req_mm = float(crop.get("water_req_mm", 450.0))
            demand_m3 = round(req_mm * 4.04686 * area, 1)
            total_demand_m3 += demand_m3
            crop_summary.append({
                "crop_name": crop.get("name", "General Crop"),
                "area_acres": area,
                "demand_m3": demand_m3
            })

        net_supplemental_water_m3 = round(max(0.0, total_demand_m3 - effective_rain_m3), 1)

        return {
            "farm_area_acres": farm_area_acres,
            "seasonal_rainfall_mm": seasonal_rainfall_mm,
            "gross_rainfall_volume_m3": rainfall_volume_m3,
            "effective_rainfall_volume_m3": effective_rain_m3,
            "total_crop_water_demand_m3": round(total_demand_m3, 1),
            "supplemental_irrigation_required_m3": net_supplemental_water_m3,
            "water_sustainability_status": "Self-Sufficient / Adequate Rainfall" if net_supplemental_water_m3 == 0.0 else "Requires Groundwater / Canal Irrigation",
            "crop_demand_breakdown": crop_summary
        }
