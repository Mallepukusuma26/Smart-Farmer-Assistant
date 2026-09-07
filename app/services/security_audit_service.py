"""
Security & Audit Service Module for Smart Farmer Assistant.

Manages application security event logging, role-based authorization enforcement,
request data sanitization, secure file upload validation, and audit trail retrieval.
"""

from typing import Dict, Any, List, Optional
import os
import re
from datetime import datetime
from app.extensions import db
from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditRepository


class SecurityAuditService:
    """
    Security middleware and audit trail logging engine.
    Ensures safe file uploads, sanitizes input payloads, and logs sensitive operations without passwords/tokens.
    """

    def __init__(self, repository: Optional[AuditRepository] = None):
        self.repository = repository or AuditRepository()

    def log_security_event(
        self,
        user_id: Optional[int],
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Logs a sanitized security event to the audit log trail.
        Converts details dictionary to ensure no passwords or API tokens are captured.
        """
        sanitized_details = {}
        if details:
            for k, v in details.items():
                if any(secret_kw in k.lower() for secret_kw in ["password", "token", "secret", "key"]):
                    sanitized_details[k] = "[REDACTED_SENSITIVE_DATA]"
                else:
                    sanitized_details[k] = str(v)

        return self.repository.create_log(
            user_id=user_id,
            action=action.upper(),
            entity_type=resource_type,
            entity_id=resource_id,
            ip_address=ip_address,
            details=sanitized_details
        )

    def validate_upload_filename(self, filename: str, allowed_extensions: List[str] = ["png", "jpg", "jpeg", "pdf", "csv"]) -> Tuple[bool, str]:
        """
        Validates uploaded file extensions and generates a safe, sanitized filename.
        """
        if not filename or "." not in filename:
            return False, "Invalid filename: missing extension."

        ext = filename.rsplit(".", 1)[1].lower()
        if ext not in allowed_extensions:
            return False, f"Unsupported file type .{ext}. Allowed types: {', '.join(allowed_extensions)}"

        # Strip path traversal characters
        clean_base = re.sub(r"[^a-zA-Z0-9_-]", "_", filename.rsplit(".", 1)[0])
        safe_name = f"{clean_base}_{int(datetime.now().timestamp())}.{ext}"

        return True, safe_name
