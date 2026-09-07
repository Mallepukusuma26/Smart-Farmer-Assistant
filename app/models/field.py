from datetime import datetime
from app.extensions import db

class Field(db.Model):
    """Field plot division entity within a Farm."""
    __tablename__ = 'fields'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False, index=True)
    field_name = db.Column(db.String(100), nullable=False, index=True)
    area = db.Column(db.Float, nullable=False, default=1.0)
    soil_type = db.Column(db.String(50), nullable=False, default='Loamy')  # Clay, Sandy, Loamy, Silt, Peaty, Chalky
    irrigation_type = db.Column(db.String(50), default='Drip')  # Drip, Sprinkler, Flood, Rainfed
    farming_method = db.Column(db.String(50), default='Conventional')  # Organic, Conventional, Hydroponic
    current_status = db.Column(db.String(30), default='Active', index=True)  # Active, Fallow, Harvested, Preparing
    drainage_quality = db.Column(db.String(30), default='Good')  # Excellent, Good, Fair, Poor
    sunlight_exposure = db.Column(db.String(30), default='Full Sun')  # Full Sun, Partial Shade, Shade
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    soil_records = db.relationship('SoilRecord', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    crop_cycles = db.relationship('CropCycle', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    fertilizer_recommendations = db.relationship('FertilizerRecommendation', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    irrigation_schedules = db.relationship('IrrigationSchedule', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    irrigation_logs = db.relationship('IrrigationLog', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    disease_detections = db.relationship('DiseaseDetection', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    yield_predictions = db.relationship('YieldPrediction', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    profit_predictions = db.relationship('ProfitPrediction', backref='field', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='field', lazy='dynamic')
    revenues = db.relationship('Revenue', backref='field', lazy='dynamic')
    boundaries = db.relationship('FieldBoundary', backref='field', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'field_name': self.field_name,
            'area': self.area,
            'soil_type': self.soil_type,
            'irrigation_type': self.irrigation_type,
            'farming_method': self.farming_method,
            'current_status': self.current_status,
            'drainage_quality': self.drainage_quality,
            'sunlight_exposure': self.sunlight_exposure,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Field id={self.id} name='{self.field_name}'>"


class FieldBoundary(db.Model):
    """Field GPS boundary coordinate point for local polygon mapping."""
    __tablename__ = 'field_boundaries'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    sequence_order = db.Column(db.Integer, nullable=False, default=1)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'sequence_order': self.sequence_order,
            'latitude': self.latitude,
            'longitude': self.longitude
        }


class FieldCropHistory(db.Model):
    """Historical records of past crops grown in this specific field plot."""
    __tablename__ = 'field_crop_histories'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False, default=2025)
    season = db.Column(db.String(30), default='Kharif')
    yield_obtained_tons = db.Column(db.Float, default=0.0)

    field = db.relationship('Field', backref=db.backref('crop_history', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_name': self.crop_name,
            'year': self.year,
            'season': self.season,
            'yield_obtained_tons': self.yield_obtained_tons
        }


class FieldSoilTrend(db.Model):
    """Historical soil nutrient trend data points for a field."""
    __tablename__ = 'field_soil_trends'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    record_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    ph_level = db.Column(db.Float, nullable=False)
    nitrogen_level = db.Column(db.Float, nullable=False)
    phosphorus_level = db.Column(db.Float, nullable=False)
    potassium_level = db.Column(db.Float, nullable=False)

    field = db.relationship('Field', backref=db.backref('soil_trends', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'record_date': self.record_date.strftime('%Y-%m-%d'),
            'ph_level': self.ph_level,
            'nitrogen_level': self.nitrogen_level,
            'phosphorus_level': self.phosphorus_level,
            'potassium_level': self.potassium_level
        }


class FieldIrrigationLog(db.Model):
    """Cumulative field irrigation summary log."""
    __tablename__ = 'field_irrigation_summary_logs'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    total_water_applied_liters = db.Column(db.Float, default=0.0)
    month_year = db.Column(db.String(20), nullable=False, default='2026-09')

    field = db.relationship('Field', backref=db.backref('summary_irrigation_logs', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'total_water_applied_liters': self.total_water_applied_liters,
            'month_year': self.month_year
        }

