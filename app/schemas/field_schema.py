from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.field import Field

class FieldSchema(BaseSchema):
    """Field plot division serialization DTO."""

    @staticmethod
    def dump_field_detail(field: Optional[Field]) -> Dict[str, Any]:
        if not field:
            return {}
        data = field.to_dict()
        data['boundary_polygon'] = [b.to_dict() for b in field.boundaries.order_by('sequence_order').all()]
        data['recent_soil'] = field.soil_records.order_by('test_date desc').first().to_dict() if field.soil_records.count() > 0 else None
        data['crop_history'] = [ch.to_dict() for ch in field.crop_history.all()]
        return data
