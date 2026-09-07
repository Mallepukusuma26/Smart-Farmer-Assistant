from datetime import datetime
from app.extensions import db

class Notification(db.Model):
    """System and action notification model."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), default='info') # info, success, warning, danger
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    link_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'category': self.category,
            'is_read': self.is_read,
            'link_url': self.link_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self):
        return f"<Notification id={self.id} title='{self.title}'>"
