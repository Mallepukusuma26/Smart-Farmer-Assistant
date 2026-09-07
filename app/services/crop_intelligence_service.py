"""
Crop Intelligence Service Module for Smart Farmer Assistant.

Provides comprehensive crop lifecycle tracking, phenological stage management,
sowing/harvesting calendar generation, crop rotation scoring, and suitability ranking.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.extensions import db
from app.models.crop import Crop
from app.repositories.crop_repository import CropRepository


class CropIntelligenceService:
    """
    Service for crop species management, phenology calculation,
    rotation sequence scoring, and multi-criteria crop selection.
    """

    def __init__(self, repository: Optional[CropRepository] = None):
        self.repository = repository or CropRepository()

    def get_crop_phenology_schedule(self, crop_name: str, sowing_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Generates estimated phenological growth stages based on sowing date.
        """
        base_date = datetime.strptime(sowing_date, "%Y-%m-%d") if sowing_date else datetime.now()
        crop_obj = self.repository.find_by_name(crop_name)
        total_days = crop_obj.duration_days if crop_obj else 120

        germination_days = int(total_days * 0.08)
        vegetative_days = int(total_days * 0.35)
        flowering_days = int(total_days * 0.25)
        maturity_days = int(total_days * 0.32)

        d1 = base_date + timedelta(days=germination_days)
        d2 = d1 + timedelta(days=vegetative_days)
        d3 = d2 + timedelta(days=flowering_days)
        d4 = d3 + timedelta(days=maturity_days)

        return {
            "crop_name": crop_name,
            "sowing_date": base_date.strftime("%Y-%m-%d"),
            "total_duration_days": total_days,
            "stages": [
                {"stage": "Germination & Emergence", "start_date": base_date.strftime("%Y-%m-%d"), "end_date": d1.strftime("%Y-%m-%d"), "duration_days": germination_days},
                {"stage": "Vegetative Growth", "start_date": d1.strftime("%Y-%m-%d"), "end_date": d2.strftime("%Y-%m-%d"), "duration_days": vegetative_days},
                {"stage": "Flowering & Grain Filling", "start_date": d2.strftime("%Y-%m-%d"), "end_date": d3.strftime("%Y-%m-%d"), "duration_days": flowering_days},
                {"stage": "Maturity & Harvest", "start_date": d3.strftime("%Y-%m-%d"), "end_date": d4.strftime("%Y-%m-%d"), "duration_days": maturity_days}
            ],
            "estimated_harvest_date": d4.strftime("%Y-%m-%d")
        }

    def evaluate_rotation_sequence(self, crop_sequence: List[str]) -> Dict[str, Any]:
        """
        Evaluates a multi-season crop rotation sequence for disease break and nutrient sustainability.
        """
        if not crop_sequence or len(crop_sequence) < 2:
            return {"score": 70.0, "status": "Acceptable", "notes": "Minimum 2 crops required for sequence evaluation."}

        score = 80.0
        notes = []

        legumes = ["chickpea", "gram", "groundnut", "soybean", "lentils", "pulses", "peas"]
        cereals = ["wheat", "rice", "paddy", "maize", "barley", "sorghum"]

        for i in range(len(crop_sequence) - 1):
            c1 = crop_sequence[i].lower()
            c2 = crop_sequence[i + 1].lower()

            if c1 == c2:
                score -= 20.0
                notes.append(f"Repeated planting of {crop_sequence[i]} increases pest and soil disease risk.")

            if (any(leg in c1 for leg in legumes) and any(cer in c2 for cer in cereals)) or \
               (any(cer in c1 for cer in cereals) and any(leg in c2 for leg in legumes)):
                score += 10.0
                notes.append(f"Rotating between {crop_sequence[i]} and {crop_sequence[i+1]} provides natural nitrogen replenishment.")

        final_score = round(max(10.0, min(100.0, score)), 1)
        status = "Excellent" if final_score >= 85.0 else ("Good" if final_score >= 70.0 else "Poor")

        return {
            "crop_sequence": crop_sequence,
            "rotation_score": final_score,
            "status": status,
            "agronomic_observations": notes
        }

    def get_crop_variety_recommendations(self, category: str = "Cereals") -> List[Dict[str, Any]]:
        """
        Returns catalog of recommended crop varieties filtered by category.
        """
        crops = Crop.query.filter(Crop.category.ilike(f"%{category}%")).all()
        results = []
        for c in crops:
            results.append({
                "id": c.id,
                "name": c.name,
                "season": c.season,
                "duration_days": c.duration_days,
                "base_yield_per_acre": c.base_yield_per_acre,
                "water_req_mm": c.water_req_mm,
                "ideal_soil_type": c.ideal_soil_type
            })
        return results
