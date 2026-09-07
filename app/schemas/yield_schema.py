from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.yield_prediction import YieldPrediction

class YieldSchema(BaseSchema):
    """ML yield prediction serialization DTO."""

    @staticmethod
    def dump_prediction_detail(prediction: Optional[YieldPrediction]) -> Dict[str, Any]:
        if not prediction:
            return {}
        data = prediction.to_dict()
        data['factors_list'] = [f.to_dict() for f in prediction.factors.all()]
        return data
