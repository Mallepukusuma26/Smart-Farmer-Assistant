from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.profit_prediction import ProfitPrediction

class ProfitSchema(BaseSchema):
    """Profitability forecast & scenario serialization DTO."""

    @staticmethod
    def dump_profit_detail(profit: Optional[ProfitPrediction]) -> Dict[str, Any]:
        if not profit:
            return {}
        data = profit.to_dict()
        data['scenarios'] = [s.to_dict() for s in profit.scenarios.all()]
        return data
