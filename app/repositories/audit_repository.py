from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.audit import AuditLog, SystemAuditLog, SecurityLog, APIAccessLog
from app.repositories.base_repository import BaseRepository

class AuditRepository(BaseRepository[AuditLog]):
    """Data Access Repository for Audit Logging, Security Event Auditing, and System Maintenance Logs."""

    def __init__(self):
        super().__init__(AuditLog)

    def log_action(self, action: str, user_id: Optional[int] = None, target_type: Optional[str] = None, target_id: Optional[int] = None, details: Optional[str] = None, ip_address: Optional[str] = None, user_agent: Optional[str] = None, status: str = 'SUCCESS') -> AuditLog:
        """Create structured audit log entry."""
        audit = AuditLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status
        )
        db.session.add(audit)
        db.session.commit()
        return audit

    def get_recent_audits(self, user_id: Optional[int] = None, action: Optional[str] = None, page: int = 1, per_page: int = 25) -> Tuple[List[AuditLog], int, int]:
        """Fetch paginated audit log entries with filter options."""
        query = db.session.query(AuditLog)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if action:
            query = query.filter_by(action=action)
        return self.paginate(page=page, per_page=per_page, query=query.order_by(AuditLog.created_at.desc()))

    def log_system_event(self, component_name: str, message: str, event_level: str = 'INFO', execution_time_ms: float = 0.0) -> SystemAuditLog:
        """Log background process or system event."""
        sys_log = SystemAuditLog(
            component_name=component_name,
            event_level=event_level,
            message=message,
            execution_time_ms=execution_time_ms
        )
        db.session.add(sys_log)
        db.session.commit()
        return sys_log

    def log_api_access(self, endpoint: str, http_method: str, status_code: int, response_time_ms: float, user_id: Optional[int] = None) -> APIAccessLog:
        """Log REST API route latency and status code."""
        access_log = APIAccessLog(
            endpoint=endpoint,
            http_method=http_method,
            status_code=status_code,
            response_time_ms=response_time_ms,
            user_id=user_id
        )
        db.session.add(access_log)
        db.session.commit()
        return access_log
