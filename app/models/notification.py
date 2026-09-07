from datetime import datetime
from typing import Dict, Any, List, Optional
from app.extensions import db

class Notification(db.Model):
    """System and action notification model."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), default='info') # info, success, warning, danger
    notification_type = db.Column(db.String(50), default='Irrigation Alert') # Irrigation Alert, Fertilizer Reminder, Disease Alert, Crop Reminder, Harvest Reminder, Financial Alert, System Notification
    priority = db.Column(db.String(20), default='Medium') # Low, Medium, High, Urgent
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)
    link_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def mark_read(self) -> None:
        """Mark notification as read with current timestamp."""
        self.is_read = True
        self.read_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'category': self.category,
            'notification_type': self.notification_type,
            'priority': self.priority,
            'is_read': self.is_read,
            'read_at': self.read_at.strftime('%Y-%m-%d %H:%M') if self.read_at else None,
            'link_url': self.link_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<Notification id={self.id} title='{self.title}'>"


class NotificationTemplate(db.Model):
    """Reusable notification message template catalog."""
    __tablename__ = 'notification_templates'

    id = db.Column(db.Integer, primary_key=True)
    event_key = db.Column(db.String(100), unique=True, nullable=False)
    title_template = db.Column(db.String(150), nullable=False)
    body_template = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), default='info')
    default_priority = db.Column(db.String(20), default='Medium')

    def render(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Render template parameters with contextual dictionary."""
        title = self.title_template
        body = self.body_template
        for key, val in context.items():
            title = title.replace(f"{{{key}}}", str(val))
            body = body.replace(f"{{{key}}}", str(val))
        return {'title': title, 'message': body}

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'event_key': self.event_key,
            'title_template': self.title_template,
            'body_template': self.body_template,
            'category': self.category,
            'default_priority': self.default_priority
        }


class UserNotificationSetting(db.Model):
    """User preference settings for notification channels and alerts."""
    __tablename__ = 'user_notification_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    enable_irrigation_alerts = db.Column(db.Boolean, default=True)
    enable_fertilizer_reminders = db.Column(db.Boolean, default=True)
    enable_disease_warnings = db.Column(db.Boolean, default=True)
    enable_financial_reports = db.Column(db.Boolean, default=True)
    enable_system_updates = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notification_settings', uselist=False, cascade='all, delete-orphan'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'enable_irrigation_alerts': self.enable_irrigation_alerts,
            'enable_fertilizer_reminders': self.enable_fertilizer_reminders,
            'enable_disease_warnings': self.enable_disease_warnings,
            'enable_financial_reports': self.enable_financial_reports,
            'enable_system_updates': self.enable_system_updates
        }

