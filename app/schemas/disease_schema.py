from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.disease import DiseaseDetection, Disease

class DiseaseSchema(BaseSchema):
    """Disease diagnosis & leaf image inference serialization DTO."""

    @staticmethod
    def dump_detection_detail(detection: Optional[DiseaseDetection]) -> Dict[str, Any]:
        if not detection:
            return {}
        data = detection.to_dict()
        if hasattr(detection, 'feature_vector') and detection.feature_vector:
            data['feature_vector'] = detection.feature_vector.to_dict()
        return data
