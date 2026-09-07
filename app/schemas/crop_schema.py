from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.crop import Crop

class CropSchema(BaseSchema):
    """Crop catalog species serialization DTO."""

    @staticmethod
    def dump_crop_detail(crop: Optional[Crop]) -> Dict[str, Any]:
        if not crop:
            return {}
        data = crop.to_dict()
        data['varieties'] = [v.to_dict() for v in crop.varieties.all()]
        data['pests_diseases'] = [pd.to_dict() for pd in crop.pests_diseases.all()]
        data['growth_stages'] = [gs.to_dict() for gs in crop.growth_stages.all()]
        return data
