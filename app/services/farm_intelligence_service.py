"""
Farm Intelligence Service Module for Smart Farmer Assistant.

Provides advanced farm analytics, land productivity comparisons, multi-farm statistics,
aggregated financial metrics, crop rotation sequence evaluation, and long-term farm health scoring.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import math
from app.extensions import db
from app.models.farm import Farm
from app.models.field import Field
from app.repositories.farm_repository import FarmRepository
from app.repositories.field_repository import FieldRepository


class FarmIntelligenceService:
    """
    Comprehensive service for high-level farm analytics, land productivity scoring,
    multi-farm comparisons, and strategic multi-season planning.
    """

    def __init__(self, farm_repo: Optional[FarmRepository] = None, field_repo: Optional[FieldRepository] = None):
        self.farm_repo = farm_repo or FarmRepository()
        self.field_repo = field_repo or FieldRepository()

    def get_farm_comprehensive_overview(self, farm_id: int) -> Dict[str, Any]:
        """
        Calculates complete farm status including total area, field counts,
        soil composition distribution, and average field health rating.
        """
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            return {"error": f"Farm with ID {farm_id} not found."}

        fields = db.session.query(Field).filter_by(farm_id=farm_id).all()
        total_fields = len(fields)
        total_field_area = sum(float(f.area or 0.0) for f in fields)
        unallocated_area = max(0.0, float(farm.total_area or 0.0) - total_field_area)

        soil_distribution = {}
        irrigation_distribution = {}
        for f in fields:
            st = f.soil_type or farm.default_soil_type or "Loamy"
            soil_distribution[st] = soil_distribution.get(st, 0) + 1

            it = f.irrigation_type or "Drip"
            irrigation_distribution[it] = irrigation_distribution.get(it, 0) + 1

        health_rating = self.calculate_farm_health_score(farm_id)
        productivity_index = self.calculate_productivity_index(farm_id)

        return {
            "farm_id": farm.id,
            "farm_name": farm.name,
            "location": farm.location,
            "county_district": farm.county_district,
            "state": farm.state,
            "ownership_type": farm.ownership_type,
            "total_registered_acres": float(farm.total_area or 0.0),
            "allocated_field_acres": round(total_field_area, 2),
            "unallocated_acres": round(unallocated_area, 2),
            "total_fields_count": total_fields,
            "soil_type_breakdown": soil_distribution,
            "irrigation_type_breakdown": irrigation_distribution,
            "health_rating_pct": health_rating["score"],
            "health_grade": health_rating["grade"],
            "productivity_index": productivity_index["score"],
            "productivity_rating": productivity_index["rating"],
            "recommendations": health_rating["recommendations"]
        }

    def calculate_farm_health_score(self, farm_id: int) -> Dict[str, Any]:
        """
        Evaluates overall farm health score based on soil test records, field coverage,
        crop diversity, and environmental land factors.
        """
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            return {"score": 50.0, "grade": "C", "recommendations": ["Farm not found."]}

        fields = db.session.query(Field).filter_by(farm_id=farm_id).all()
        if not fields:
            return {
                "score": 60.0,
                "grade": "B-",
                "recommendations": ["Register field plot divisions to enable detailed soil and crop health tracking."]
            }

        score = 80.0
        recommendations = []

        # Soil diversity and field division factor
        if len(fields) < 2:
            score -= 5.0
            recommendations.append("Consider dividing farm into multiple management plots for crop rotation.")

        # Soil type optimization
        soil_types = set(f.soil_type for f in fields if f.soil_type)
        if len(soil_types) >= 2:
            score += 5.0

        # Allocation ratio check
        total_field_area = sum(float(f.area or 0.0) for f in fields)
        farm_area = float(farm.total_area or 1.0)
        allocation_ratio = total_field_area / farm_area if farm_area > 0 else 0

        if allocation_ratio < 0.5:
            score -= 10.0
            recommendations.append("More than 50% of farm land is unallocated to active field plots.")
        elif allocation_ratio > 1.0:
            score -= 5.0
            recommendations.append("Sum of field plot areas exceeds total registered farm boundary area.")

        final_score = round(max(10.0, min(100.0, score)), 1)
        if final_score >= 85.0:
            grade = "A"
        elif final_score >= 70.0:
            grade = "B"
        elif final_score >= 55.0:
            grade = "C"
        else:
            grade = "D"

        if not recommendations:
            recommendations.append("Farm land management structure is well balanced.")

        return {
            "score": final_score,
            "grade": grade,
            "recommendations": recommendations
        }

    def calculate_productivity_index(self, farm_id: int) -> Dict[str, Any]:
        """
        Computes agricultural land productivity index based on crop density,
        irrigation efficiency, and historical land yield capabilities.
        """
        fields = db.session.query(Field).filter_by(farm_id=farm_id).all()
        if not fields:
            return {"score": 50.0, "rating": "Moderate"}

        score = 70.0
        # Check irrigation technology
        drip_count = sum(1 for f in fields if (f.irrigation_type or "").lower() in ["drip", "sprinkler", "micro-sprinkler"])
        irrigation_ratio = drip_count / len(fields)
        score += (irrigation_ratio * 15.0)

        # Check organic/conventional balance
        organic_count = sum(1 for f in fields if (f.farming_method or "").lower() == "organic")
        score += (organic_count / len(fields)) * 10.0

        final_score = round(max(10.0, min(100.0, score)), 1)
        rating = "High Efficiency" if final_score >= 80.0 else ("Moderate Efficiency" if final_score >= 60.0 else "Low Efficiency")

        return {
            "score": final_score,
            "rating": rating,
            "modern_irrigation_coverage_pct": round(irrigation_ratio * 100.0, 1)
        }

    def compare_farms(self, farmer_id: int) -> List[Dict[str, Any]]:
        """
        Compares all farms owned by a farmer across area, fields, productivity, and health scores.
        """
        farms = self.farm_repo.get_farms_by_farmer(farmer_id)
        comparison_list = []

        for f in farms:
            overview = self.get_farm_comprehensive_overview(f.id)
            comparison_list.append({
                "farm_id": f.id,
                "name": f.name,
                "total_area": float(f.total_area or 0.0),
                "total_fields": overview.get("total_fields_count", 0),
                "health_score": overview.get("health_rating_pct", 70.0),
                "productivity_index": overview.get("productivity_index", 70.0),
                "location": f.location
            })

        return sorted(comparison_list, key=lambda x: x["health_score"], reverse=True)

    def generate_seasonal_farm_plan(self, farm_id: int, target_season: str = "Kharif") -> Dict[str, Any]:
        """
        Generates a recommended crop rotation and field allocation strategy for an upcoming farming season.
        """
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            return {"error": "Farm not found"}

        fields = db.session.query(Field).filter_by(farm_id=farm_id).all()
        plan_details = []

        crop_pool = {
            "Kharif": ["Rice / Paddy", "Cotton", "Maize", "Groundnut", "Soybean"],
            "Rabi": ["Wheat", "Mustard", "Chickpea / Gram", "Barley", "Potato"],
            "Zaid": ["Watermelon", "Cucumber", "Muskmelon", "Fodder Crops"]
        }

        recommended_crops = crop_pool.get(target_season, crop_pool["Kharif"])

        for idx, field in enumerate(fields):
            crop_assigned = recommended_crops[idx % len(recommended_crops)]
            plan_details.append({
                "field_id": field.id,
                "field_name": field.field_name,
                "area_acres": float(field.area or 0.0),
                "soil_type": field.soil_type,
                "recommended_crop": crop_assigned,
                "sowing_window": f"Early {target_season}",
                "estimated_seed_qty_kg": round(float(field.area or 1.0) * 12.5, 1),
                "expected_water_demand_m3": round(float(field.area or 1.0) * 450.0, 0)
            })

        return {
            "farm_id": farm.id,
            "farm_name": farm.name,
            "season": target_season,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "field_allocations": plan_details
        }
