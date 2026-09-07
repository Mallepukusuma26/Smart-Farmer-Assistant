from datetime import datetime
from app.extensions import db

class IrrigationSchedule(db.Model):
    """Calculated irrigation schedule entity."""
    __tablename__ = 'irrigation_schedules'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_cycle_id = db.Column(db.Integer, db.ForeignKey('crop_cycles.id', ondelete='SET NULL'), nullable=True)
    water_required_liters = db.Column(db.Float, nullable=False, default=1000.0)
    next_irrigation_date = db.Column(db.Date, nullable=False)
    frequency_days = db.Column(db.Integer, default=5)
    duration_minutes = db.Column(db.Integer, default=60)
    method = db.Column(db.String(50), default='Drip')
    status = db.Column(db.String(30), default='Scheduled') # Scheduled, Completed, Skipped
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_cycle_id': self.crop_cycle_id,
            'water_required_liters': self.water_required_liters,
            'next_irrigation_date': self.next_irrigation_date.strftime('%Y-%m-%d') if self.next_irrigation_date else None,
            'frequency_days': self.frequency_days,
            'duration_minutes': self.duration_minutes,
            'method': self.method,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<IrrigationSchedule id={self.id} field_id={self.field_id} status='{self.status}'>"


class IrrigationLog(db.Model):
    """History log of completed irrigation events."""
    __tablename__ = 'irrigation_logs'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    irrigation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    water_used_liters = db.Column(db.Float, nullable=False, default=1000.0)
    duration_minutes = db.Column(db.Integer, default=60)
    rainfall_observed_mm = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'irrigation_date': self.irrigation_date.strftime('%Y-%m-%d %H:%M'),
            'water_used_liters': self.water_used_liters,
            'duration_minutes': self.duration_minutes,
            'rainfall_observed_mm': self.rainfall_observed_mm,
            'notes': self.notes
        }

    def __repr__(self):
        return f"<IrrigationLog id={self.id} water_used_liters={self.water_used_liters}>"
