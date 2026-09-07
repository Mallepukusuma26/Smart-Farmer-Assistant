"""
Water Source Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing WaterSource entity persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.water_source import WaterSource
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class WaterSourceRepository(BaseRepository[WaterSource]):
    """
    Repository handling database operations for WaterSource entities.
    """

    def __init__(self):
        super().__init__(WaterSource)

    def get_by_farm(self, farm_id: int) -> List[WaterSource]:
        """
        Retrieves water sources associated with a farm.
        """
        return self.model.query.filter_by(farm_id=farm_id).order_by(self.model.source_name.asc()).all()
