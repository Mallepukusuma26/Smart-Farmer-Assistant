"""
Field Service Module for Smart Farmer Assistant.
Manages field CRUD operations, boundary telemetry, soil profiles, and crop assignments.
"""

from typing import List, Dict, Any, Optional
from app.extensions import db
from app.models.field import Field
from app.repositories.field_repository import FieldRepository
import logging

logger = logging.getLogger(__name__)


class FieldService:
    """Business logic service for managing farm fields."""

    def __init__(self, field_repo: Optional[FieldRepository] = None):
        self.field_repo = field_repo or FieldRepository()

    def get_field(self, field_id: int) -> Optional[Field]:
        return self.field_repo.get_by_id(field_id)

    def get_fields_by_farm(self, farm_id: int) -> List[Field]:
        return self.field_repo.get_by_farm_id(farm_id)

    def create_field(self, data: Dict[str, Any]) -> Field:
        return self.field_repo.create(data)

    def update_field(self, field_id: int, data: Dict[str, Any]) -> Optional[Field]:
        return self.field_repo.update(field_id, data)

    def delete_field(self, field_id: int) -> bool:
        return self.field_repo.delete(field_id)
