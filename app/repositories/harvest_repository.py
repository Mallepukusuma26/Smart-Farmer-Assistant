"""
Harvest Log Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing HarvestLog entity persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.harvest_log import HarvestLog
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class HarvestRepository(BaseRepository[HarvestLog]):
    """
    Repository handling data access for HarvestLog entities.
    """

    def __init__(self):
        super().__init__(HarvestLog)

    def get_by_farmer(self, farmer_id: int) -> List[HarvestLog]:
        """
        Retrieves harvest logs for a farmer.
        """
        return self.model.query.filter_by(farmer_id=farmer_id).order_by(self.model.harvest_date.desc()).all()

    def get_by_farmer_paginated(
        self,
        farmer_id: int,
        page: int = 1,
        per_page: int = 15,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[HarvestLog], int]:
        """
        Retrieves paginated harvest logs for a farmer.
        """
        query = self.model.query.filter_by(farmer_id=farmer_id)
        if filters and "crop_name" in filters:
            query = query.filter(self.model.crop_name.ilike(f"%{filters['crop_name']}%"))

        total = query.count()
        items = query.order_by(self.model.harvest_date.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return items, total
