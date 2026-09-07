"""
Machinery Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing Machinery asset persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.machinery import Machinery
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class MachineryRepository(BaseRepository[Machinery]):
    """
    Repository handling data access and database operations for Machinery assets.
    """

    def __init__(self):
        super().__init__(Machinery)

    def get_by_farmer(self, farmer_id: int) -> List[Machinery]:
        """
        Retrieves machinery assets owned by a farmer.
        """
        return self.model.query.filter_by(farmer_id=farmer_id).order_by(self.model.name.asc()).all()

    def get_by_farmer_paginated(
        self,
        farmer_id: int,
        page: int = 1,
        per_page: int = 15,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Machinery], int]:
        """
        Retrieves paginated machinery assets for a farmer.
        """
        query = self.model.query.filter_by(farmer_id=farmer_id)
        if filters and "equipment_type" in filters:
            query = query.filter_by(equipment_type=filters["equipment_type"])

        total = query.count()
        items = query.order_by(self.model.name.asc()).offset((page - 1) * per_page).limit(per_page).all()
        return items, total
