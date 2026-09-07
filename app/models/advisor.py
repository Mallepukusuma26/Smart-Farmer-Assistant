from datetime import datetime
from app.extensions import db

class Advisor(db.Model):
    """Agricultural Advisor profile entity."""
    __tablename__ = 'advisors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assigned_farmers = db.relationship('Farmer', backref='assigned_advisor', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'qualification': self.qualification,
            'specialization': self.specialization,
            'region': self.region,
            'phone': self.phone,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Advisor id={self.id} name='{self.full_name}'>"
