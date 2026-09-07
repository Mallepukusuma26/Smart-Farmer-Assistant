from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.notification import Notification, NotificationTemplate, UserNotificationSetting
from app.repositories.base_repository import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    """Data Access Repository for Notifications, Templates, and User Preferences."""

    def __init__(self):
        super().__init__(Notification)

    def create_notification(self, user_id: int, title: str, message: str, category: str = 'info', notification_type: str = 'Irrigation Alert', priority: str = 'Medium', link_url: Optional[str] = None) -> Notification:
        """Create and deliver user notification."""
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            category=category,
            notification_type=notification_type,
            priority=priority,
            link_url=link_url
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    def get_user_notifications(self, user_id: int, unread_only: bool = False, limit: int = 50) -> List[Notification]:
        """Fetch notifications for user."""
        query = db.session.query(Notification).filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

    def count_unread(self, user_id: int) -> int:
        """Count unread notifications for user badge."""
        return db.session.query(func.count(Notification.id)).filter_by(user_id=user_id, is_read=False).scalar() or 0

    def mark_all_read(self, user_id: int) -> int:
        """Mark all unread notifications read for user."""
        now = datetime.utcnow()
        count = db.session.query(Notification).filter_by(user_id=user_id, is_read=False).update(
            {Notification.is_read: True, Notification.read_at: now}, synchronize_session=False
        )
        db.session.commit()
        return count

    def get_template(self, event_key: str) -> Optional[NotificationTemplate]:
        """Fetch notification template by event key."""
        return db.session.query(NotificationTemplate).filter_by(event_key=event_key).first()
