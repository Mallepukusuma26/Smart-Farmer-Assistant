from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.soil import SoilRecord

class SoilSchema(BaseSchema):
    """Soil analysis & amendment serialization DTO."""

    @staticmethod
    def dump_soil_detail(soil: Optional[SoilRecord]) -> Dict[str, Any]:
        if not soil:
            return {}
        data = soil.to_dict()
        data['improvement_plans'] = [plan.to_dict() for plan in soil.improvement_plans.all()]
        return data
