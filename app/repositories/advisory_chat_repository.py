"""
Advisory Chat Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing AdvisoryChat persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.advisory_chat import AdvisoryChat
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class AdvisoryChatRepository(BaseRepository[AdvisoryChat]):
    """
    Repository handling database operations for AdvisoryChat message threads.
    """

    def __init__(self):
        super().__init__(AdvisoryChat)

    def get_by_case(self, case_id: int) -> List[AdvisoryChat]:
        """
        Retrieves consultation messages for a specific case ID.
        """
        return self.model.query.filter_by(case_id=case_id).order_by(self.model.created_at.asc()).all()
