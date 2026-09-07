from datetime import datetime
from app.extensions import db

class Crop(db.Model):
    """Agricultural crop catalog & reference parameters."""
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False) # Cereal, Pulse, Oilseed, Vegetable, Fruit, Cash Crop
    season = db.Column(db.String(50), nullable=False)   # Kharif, Rabi, Zaid, Perennial
    min_ph = db.Column(db.Float, default=5.5)
    max_ph = db.Column(db.Float, default=7.5)
    min_temp = db.Column(db.Float, default=15.0)       # deg Celsius
    max_temp = db.Column(db.Float, default=35.0)
    min_rainfall = db.Column(db.Float, default=400.0)   # mm
    max_rainfall = db.Column(db.Float, default=1500.0)
    min_n = db.Column(db.Float, default=60.0)
    min_p = db.Column(db.Float, default=30.0)
    min_k = db.Column(db.Float, default=40.0)
    duration_days = db.Column(db.Integer, default=120)
    base_yield_per_acre = db.Column(db.Float, default=2.5) # metric tons
    water_req_mm = db.Column(db.Float, default=500.0)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    crop_cycles = db.relationship('CropCycle', backref='crop', lazy='dynamic')
    fertilizer_recommendations = db.relationship('FertilizerRecommendation', backref='crop', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'season': self.season,
            'ph_range': f"{self.min_ph} - {self.max_ph}",
            'temp_range': f"{self.min_temp}°C - {self.max_temp}°C",
            'rainfall_range': f"{self.min_rainfall}mm - {self.max_rainfall}mm",
            'duration_days': self.duration_days,
            'base_yield_per_acre': self.base_yield_per_acre,
            'water_req_mm': self.water_req_mm,
            'description': self.description
        }

    def __repr__(self):
        return f"<Crop id={self.id} name='{self.name}'>"


class CropCycle(db.Model):
    """Active or past crop growth cycle on a field."""
    __tablename__ = 'crop_cycles'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='RESTRICT'), nullable=False)
    sowing_date = db.Column(db.Date, nullable=False)
    expected_harvest_date = db.Column(db.Date, nullable=False)
    actual_harvest_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='Growing') # Sown, Growing, Flowering, Harvesting, Completed, Failed
    acreage = db.Column(db.Float, default=1.0)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    irrigation_schedules = db.relationship('IrrigationSchedule', backref='crop_cycle', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else 'Unknown',
            'sowing_date': self.sowing_date.strftime('%Y-%m-%d') if self.sowing_date else None,
            'expected_harvest_date': self.expected_harvest_date.strftime('%Y-%m-%d') if self.expected_harvest_date else None,
            'actual_harvest_date': self.actual_harvest_date.strftime('%Y-%m-%d') if self.actual_harvest_date else None,
            'status': self.status,
            'acreage': self.acreage,
            'notes': self.notes
        }

    def __repr__(self):
        return f"<CropCycle id={self.id} crop_id={self.crop_id} status='{self.status}'>"
