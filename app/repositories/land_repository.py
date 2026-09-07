"""
Land Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing LandRecord persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.land_record import LandRecord
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class LandRepository(BaseRepository[LandRecord]):
    """
    Repository handling database operations for LandRecord entities.
    """

    def __init__(self):
        super().__init__(LandRecord)

    def get_by_farm(self, farm_id: int) -> List[LandRecord]:
        """
        Retrieves land records associated with a farm.
        """
        return self.model.query.filter_by(farm_id=farm_id).order_by(self.model.survey_number.asc()).all()

    def get_by_survey_number(self, survey_number: str) -> Optional[LandRecord]:
        """
        Looks up land record by cadastral survey number.
        """
        return self.model.query.filter_by(survey_number=survey_number).first()
