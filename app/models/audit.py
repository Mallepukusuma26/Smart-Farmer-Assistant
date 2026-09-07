from datetime import datetime
from typing import Dict, Any, List, Optional
from app.extensions import db

class AuditLog(db.Model):
    """System activity and security audit trail model."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    action = db.Column(db.String(100), nullable=False) # e.g., USER_LOGIN, FARM_CREATE, DISEASE_DETECT, MODEL_PREDICT
    target_type = db.Column(db.String(50), nullable=True)
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='SUCCESS') # SUCCESS, FAILURE, DENIED
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'System / Anonymous',
            'action': self.action,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self) -> str:
        return f"<AuditLog id={self.id} action='{self.action}' user_id={self.user_id}>"


class SystemAuditLog(db.Model):
    """System maintenance and background worker audit records."""
    __tablename__ = 'system_audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    component_name = db.Column(db.String(100), nullable=False) # Database, ML_Engine, Backup, Scheduler
    event_level = db.Column(db.String(20), default='INFO') # INFO, WARNING, ERROR, CRITICAL
    message = db.Column(db.Text, nullable=False)
    execution_time_ms = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'component_name': self.component_name,
            'event_level': self.event_level,
            'message': self.message,
            'execution_time_ms': round(self.execution_time_ms, 2),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class SecurityLog(db.Model):
    """Dedicated security event logging for brute force, unauthorized access, and CSRF failures."""
    __tablename__ = 'security_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    event_type = db.Column(db.String(100), nullable=False) # FAILED_LOGIN, PASSWORD_RESET, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED
    severity = db.Column(db.String(20), default='WARNING') # LOW, MEDIUM, HIGH, CRITICAL
    source_ip = db.Column(db.String(45), nullable=False)
    raw_payload_snippet = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'severity': self.severity,
            'source_ip': self.source_ip,
            'raw_payload_snippet': self.raw_payload_snippet,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class APIAccessLog(db.Model):
    """Performance and access log for internal REST endpoints."""
    __tablename__ = 'api_access_logs'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(150), nullable=False)
    http_method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    response_time_ms = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'endpoint': self.endpoint,
            'http_method': self.http_method,
            'status_code': self.status_code,
            'response_time_ms': round(self.response_time_ms, 2),
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

