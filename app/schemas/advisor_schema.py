from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.advisor import Advisor, AdvisorCase

class AdvisorSchema(BaseSchema):
    """Advisor profile & consultation case serialization DTO."""

    @staticmethod
    def dump_case_detail(case: Optional[AdvisorCase]) -> Dict[str, Any]:
        if not case:
            return {}
        data = case.to_dict()
        data['consultations'] = [c.to_dict() for c in case.consultations.order_by('created_at asc').all()]
        return data
