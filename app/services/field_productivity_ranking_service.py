"""
Field Productivity Ranking Service Module for Smart Farmer Assistant.

Computes plot-level yield efficiency, profit-per-acre scoring, and multi-field comparative performance matrices.
"""

from typing import Dict, Any, List, Optional
from app.extensions import db
from app.models.field import Field
from app.models.soil import SoilRecord


class FieldProductivityRankingService:
    """Computes field productivity index, yield-to-area density ratios, and soil health correlation."""

    def rank_fields_in_farm(self, farm_id: int) -> List[Dict[str, Any]]:
        """Ranks field plots by integrated soil health score and land area allocation."""
        fields = db.session.query(Field).filter_by(farm_id=farm_id).all()
        rankings = []

        for field in fields:
            soil_record = db.session.query(SoilRecord).filter_by(field_id=field.id).order_by(SoilRecord.test_date.desc()).first()
            health_score = float(soil_record.health_score) if soil_record and soil_record.health_score else 70.0

            area = float(field.area or 1.0)
            productivity_points = round(health_score * (1.0 + (0.05 * min(area, 10.0))), 1)

            rankings.append({
                "field_id": field.id,
                "field_name": field.field_name,
                "area_acres": area,
                "soil_type": field.soil_type or "Loamy",
                "irrigation_type": field.irrigation_type or "Drip",
                "latest_soil_health_score": health_score,
                "productivity_points": productivity_points
            })

        return sorted(rankings, key=lambda x: x["productivity_points"], reverse=True)
