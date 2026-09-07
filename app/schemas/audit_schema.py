from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.audit import AuditLog

class AuditSchema(BaseSchema):
    """Audit log serialization DTO."""

    @staticmethod
    def dump_audit_detail(audit: Optional[AuditLog]) -> Dict[str, Any]:
        if not audit:
            return {}
        return audit.to_dict()
