"""
Advanced Search & Filtering Service Module for Smart Farmer Assistant.

Provides unified, multi-attribute keyword searching, category filtering,
date range filtering, and paginated response structures across all application models.
"""

from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import or_, and_
from app.extensions import db
from app.models.farm import Farm
from app.models.field import Field
from app.models.crop import Crop
from app.models.soil import SoilRecord


class AdvancedSearchService:
    """
    Search infrastructure for multi-field filtering, keyword indexing, and pagination.
    """

    def search_all_entities(self, keyword: str, limit: int = 10) -> Dict[str, Any]:
        """
        Executes global keyword search across Farms, Fields, Crops, and Soil records.
        """
        term = f"%{keyword.strip()}%" if keyword else "%"

        farms = db.session.query(Farm).filter(
            or_(Farm.name.ilike(term), Farm.location.ilike(term), Farm.state.ilike(term))
        ).limit(limit).all()

        fields = db.session.query(Field).filter(
            or_(Field.field_name.ilike(term), Field.soil_type.ilike(term), Field.irrigation_type.ilike(term))
        ).limit(limit).all()

        crops = db.session.query(Crop).filter(
            or_(Crop.name.ilike(term), Crop.category.ilike(term), Crop.season.ilike(term))
        ).limit(limit).all()

        return {
            "query": keyword,
            "farms_found": [{"id": f.id, "name": f.name, "location": f.location} for f in farms],
            "fields_found": [{"id": f.id, "name": f.field_name, "soil_type": f.soil_type} for f in fields],
            "crops_found": [{"id": c.id, "name": c.name, "category": c.category, "season": c.season} for c in crops]
        }

    def filter_soil_records(
        self,
        min_ph: Optional[float] = None,
        max_ph: Optional[float] = None,
        min_health: Optional[float] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Filters soil test records by pH range and minimum health score.
        """
        query = db.session.query(SoilRecord)
        if min_ph is not None:
            query = query.filter(SoilRecord.ph >= min_ph)
        if max_ph is not None:
            query = query.filter(SoilRecord.ph <= max_ph)
        if min_health is not None:
            query = query.filter(SoilRecord.health_score >= min_health)

        total = query.count()
        records = query.order_by(SoilRecord.test_date.desc()).offset((page - 1) * per_page).limit(per_page).all()

        return [r.to_dict() for r in records], total
