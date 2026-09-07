from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.report import Report

class ReportSchema(BaseSchema):
    """Report file metadata serialization DTO."""

    @staticmethod
    def dump_report_detail(report: Optional[Report]) -> Dict[str, Any]:
        if not report:
            return {}
        return report.to_dict()
