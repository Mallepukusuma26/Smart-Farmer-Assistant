from datetime import datetime
from app.extensions import db

class Field(db.Model):
    """Field entity within a Farm."""
    __tablename__ = 'fields'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float, nullable=False, default=1.0)
    soil_type = db.Column(db.String(50), nullable=False, default='Loamy')  # Clay, Sandy, Loamy, Silt, Peaty, Chalky
    irrigation_type = db.Column(db.String(50), default='Drip')  # Drip, Sprinkler, Flood, Rainfed
    farming_method = db.Column(db.String(50), default='Conventional')  # Organic, Conventional, Hydroponic
    current_status = db.Column(db.String(30), default='Active')  # Active, Fallow, Harvested
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

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

    def latest_soil_record(self):
        return self.soil_records.order_by(SoilRecord.test_date.desc()).first()

    def latest_crop_cycle(self):
        return self.crop_cycles.order_by(CropCycle.sowing_date.desc()).first()

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
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Field id={self.id} name='{self.field_name}'>"
