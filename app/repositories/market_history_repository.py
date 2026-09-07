"""
Market History Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing MarketPriceHistory persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.market_price_history import MarketPriceHistory
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class MarketHistoryRepository(BaseRepository[MarketPriceHistory]):
    """
    Repository handling database operations for MarketPriceHistory entities.
    """

    def __init__(self):
        super().__init__(MarketPriceHistory)

    def get_by_crop(self, crop_name: str, limit: int = 30) -> List[MarketPriceHistory]:
        """
        Retrieves price history for a crop commodity.
        """
        return self.model.query.filter(self.model.crop_name.ilike(f"%{crop_name}%")).order_by(self.model.price_date.desc()).limit(limit).all()
