"""
Advisory Chat SQLAlchemy Model for Smart Farmer Assistant.

Stores consultation message threads between Farmers and Agricultural Advisors,
image attachments, recommendation notes, and read receipts.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class AdvisoryChat(db.Model):
    """
    SQLAlchemy model representing a consultation message thread between a farmer and an agricultural advisor.
    """
    __tablename__ = "advisory_chats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey("advisor_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_role = db.Column(db.String(20), nullable=False)  # farmer, advisor, admin
    message_text = db.Column(db.Text, nullable=False)
    attachment_path = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    case = db.relationship("AdvisorCase", backref=db.backref("chat_messages", lazy="dynamic"))
    sender = db.relationship("User", backref=db.backref("sent_advisory_messages", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "case_id": self.case_id,
            "sender_id": self.sender_id,
            "sender_role": self.sender_role,
            "sender_name": self.sender.full_name or self.sender.username if self.sender else "User",
            "message_text": self.message_text,
            "attachment_path": self.attachment_path,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat()
        }
