from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.farm import Farm

class FarmSchema(BaseSchema):
    """Farm property serialization DTO."""

    @staticmethod
    def dump_farm_detail(farm: Optional[Farm]) -> Dict[str, Any]:
        if not farm:
            return {}
        data = farm.to_dict()
        if farm.location_details:
            data['location_gps'] = farm.location_details.to_dict()
        data['fields_list'] = [field.to_dict() for field in farm.fields.all()]
        data['equipment_list'] = [eq.to_dict() for eq in farm.equipment.all()]
        data['certifications_list'] = [cert.to_dict() for cert in farm.certifications.all()]
        return data
