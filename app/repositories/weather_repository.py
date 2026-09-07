"""
Weather Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing WeatherLog entity persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.weather_log import WeatherLog
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class WeatherRepository(BaseRepository[WeatherLog]):
    """
    Repository handling data access for WeatherLog entities.
    """

    def __init__(self):
        super().__init__(WeatherLog)

    def get_by_farm(self, farm_id: int) -> List[WeatherLog]:
        """
        Retrieves weather logs for a specific farm.
        """
        return self.model.query.filter_by(farm_id=farm_id).order_by(self.model.log_date.desc()).all()
