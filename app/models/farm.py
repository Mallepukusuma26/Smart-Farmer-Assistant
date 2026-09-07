from datetime import datetime
from app.extensions import db

class Farm(db.Model):
    """Farm entity representing a farmer's property."""
    __tablename__ = 'farms'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    total_area = db.Column(db.Float, nullable=False, default=1.0)
    unit = db.Column(db.String(20), default='Acres', nullable=False)
    ownership_type = db.Column(db.String(30), default='Owned')  # Owned, Leased, Rented
    default_soil_type = db.Column(db.String(50), default='Loamy')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    fields = db.relationship('Field', backref='farm', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='farm', lazy='dynamic')
    revenues = db.relationship('Revenue', backref='farm', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'name': self.name,
            'location': self.location,
            'total_area': self.total_area,
            'unit': self.unit,
            'ownership_type': self.ownership_type,
            'default_soil_type': self.default_soil_type,
            'notes': self.notes,
            'field_count': self.fields.count(),
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Farm id={self.id} name='{self.name}'>"
