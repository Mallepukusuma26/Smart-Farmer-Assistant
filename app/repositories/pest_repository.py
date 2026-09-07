"""
Pest Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing PestRecord SQLAlchemy persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.pest_record import PestRecord
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class PestRepository(BaseRepository[PestRecord]):
    """
    Repository handling data access and database operations for PestRecord entity.
    """

    def __init__(self):
        super().__init__(PestRecord)

    def get_records_by_farmer(self, farmer_id: int) -> List[PestRecord]:
        """
        Retrieves pest logs for a specific farmer.
        """
        return self.model.query.filter_by(farmer_id=farmer_id).order_by(self.model.created_at.desc()).all()

    def get_records_by_farmer_paginated(
        self,
        farmer_id: int,
        page: int = 1,
        per_page: int = 15,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[PestRecord], int]:
        """
        Retrieves paginated pest logs for a farmer.
        """
        query = self.model.query.filter_by(farmer_id=farmer_id)
        if filters:
            if "pest_name" in filters:
                query = query.filter(self.model.pest_name.ilike(f"%{filters['pest_name']}%"))
            if "field_id" in filters:
                query = query.filter_by(field_id=filters["field_id"])

        total = query.count()
        items = query.order_by(self.model.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return items, total
