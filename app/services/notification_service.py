from app.extensions import db
from app.models.notification import Notification

class NotificationService:
    """Service layer for internal notification alerts."""

    @staticmethod
    def create_notification(user_id, title, message, category='info', link_url=None):
        """Create a new local system notification."""
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            category=category,
            link_url=link_url
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_unread_notifications(user_id):
        """Get unread notifications for a user."""
        return Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.desc()).all()

    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark a notification as read."""
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notif:
            notif.is_read = True
            db.session.commit()
            return True
        return False
