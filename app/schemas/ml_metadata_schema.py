from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.ml_metadata import MLModelRegistry, MLDatasetMetadata

class MLMetadataSchema(BaseSchema):
    """Local ML Model Registry & Dataset metadata serialization DTO."""

    @staticmethod
    def dump_model_detail(model: Optional[MLModelRegistry]) -> Dict[str, Any]:
        if not model:
            return {}
        data = model.to_dict()
        data['performance_logs'] = [p.to_dict() for p in model.performance_logs.all()]
        return data
