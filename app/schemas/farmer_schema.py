from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.farmer import Farmer

class FarmerSchema(BaseSchema):
    """Farmer profile serialization DTO."""

    @staticmethod
    def dump_farmer_detail(farmer: Optional[Farmer]) -> Dict[str, Any]:
        if not farmer:
            return {}
        data = farmer.to_dict()
        if farmer.preferences:
            data['preferences'] = farmer.preferences.to_dict()
        if farmer.assigned_advisor:
            data['advisor_name'] = farmer.assigned_advisor.full_name
        data['farms_list'] = [f.to_dict() for f in farmer.farms.all()]
        return data
