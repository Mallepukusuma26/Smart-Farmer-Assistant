"""
Budget Repository Module for Smart Farmer Assistant.

Data Access Object (DAO) for managing EnterpriseBudget persistence queries.
"""

from typing import List, Optional, Tuple, Dict, Any
from app.models.enterprise_budget import EnterpriseBudget
from app.repositories.base_repository import BaseRepository
from app.extensions import db


class BudgetRepository(BaseRepository[EnterpriseBudget]):
    """
    Repository handling database operations for EnterpriseBudget entities.
    """

    def __init__(self):
        super().__init__(EnterpriseBudget)

    def get_by_farmer(self, farmer_id: int) -> List[EnterpriseBudget]:
        """
        Retrieves enterprise budgets for a farmer.
        """
        return self.model.query.filter_by(farmer_id=farmer_id).order_by(self.model.created_at.desc()).all()
