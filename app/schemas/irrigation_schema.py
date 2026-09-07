from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.irrigation import IrrigationSchedule, WaterSource

class IrrigationSchema(BaseSchema):
    """Irrigation schedule & water source serialization DTO."""

    @staticmethod
    def dump_schedule_detail(schedule: Optional[IrrigationSchedule]) -> Dict[str, Any]:
        if not schedule:
            return {}
        data = schedule.to_dict()
        if schedule.water_source:
            data['water_source_name'] = schedule.water_source.name
        return data
