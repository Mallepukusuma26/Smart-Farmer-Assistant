from datetime import datetime
from app.extensions import db

class Farmer(db.Model):
    """Farmer profile details and relations."""
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    total_land_area = db.Column(db.Float, default=0.0)
    main_crop_type = db.Column(db.String(50), nullable=True)
    experience_years = db.Column(db.Integer, default=0)
    assigned_advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    farms = db.relationship('Farm', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    revenues = db.relationship('Revenue', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'region': self.region,
            'total_land_area': self.total_land_area,
            'main_crop_type': self.main_crop_type,
            'experience_years': self.experience_years,
            'assigned_advisor_id': self.assigned_advisor_id,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Farmer id={self.id} name='{self.full_name}'>"
