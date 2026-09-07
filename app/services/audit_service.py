from flask import request
from app.extensions import db
from app.models.audit import AuditLog

class AuditService:
    """Service layer for security and operational audit logging."""

    @staticmethod
    def log(action, user_id=None, target_type=None, target_id=None, details=None):
        """Log an event in the audit trail."""
        ip = None
        try:
            if request:
                ip = request.remote_addr
        except Exception:
            ip = '127.0.0.1'

        log_item = AuditLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
            ip_address=ip
        )
        db.session.add(log_item)
        db.session.commit()
        return log_item
