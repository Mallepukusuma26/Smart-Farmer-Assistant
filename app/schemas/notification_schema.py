from typing import Dict, Any, List, Optional
from app.schemas.base_schema import BaseSchema
from app.models.notification import Notification

class NotificationSchema(BaseSchema):
    """Notification alert serialization DTO."""

    @staticmethod
    def dump_notification_summary(notifications: List[Notification], unread_count: int) -> Dict[str, Any]:
        return {
            'unread_count': unread_count,
            'notifications': [n.to_dict() for n in notifications]
        }
