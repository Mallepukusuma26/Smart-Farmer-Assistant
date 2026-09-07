from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.fertilizer import Fertilizer

class FertilizerSchema(BaseSchema):
    """Fertilizer product & inventory serialization DTO."""

    @staticmethod
    def dump_fertilizer_detail(fertilizer: Optional[Fertilizer]) -> Dict[str, Any]:
        if not fertilizer:
            return {}
        return fertilizer.to_dict()
