from datetime import datetime
from app.extensions import db

class Crop(db.Model):
    """Agricultural crop catalog & reference parameters."""
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    scientific_name = db.Column(db.String(150), nullable=True)
    category = db.Column(db.String(50), nullable=False, index=True) # Cereal, Pulse, Oilseed, Vegetable, Fruit, Cash Crop
    season = db.Column(db.String(50), nullable=False, index=True)   # Kharif, Rabi, Zaid, Perennial
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
    ideal_soil_type = db.Column(db.String(50), default='Loamy')
    description = db.Column(db.Text, nullable=True)

    # Relationships
    varieties = db.relationship('CropVariety', backref='crop', lazy='dynamic', cascade='all, delete-orphan')
    crop_cycles = db.relationship('CropCycle', backref='crop', lazy='dynamic')
    fertilizer_recommendations = db.relationship('FertilizerRecommendation', backref='crop', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'category': self.category,
            'season': self.season,
            'ph_range': f"{self.min_ph} - {self.max_ph}",
            'temp_range': f"{self.min_temp}°C - {self.max_temp}°C",
            'rainfall_range': f"{self.min_rainfall}mm - {self.max_rainfall}mm",
            'min_n': self.min_n,
            'min_p': self.min_p,
            'min_k': self.min_k,
            'duration_days': self.duration_days,
            'base_yield_per_acre': self.base_yield_per_acre,
            'water_req_mm': self.water_req_mm,
            'ideal_soil_type': self.ideal_soil_type,
            'description': self.description
        }

    def __repr__(self):
        return f"<Crop id={self.id} name='{self.name}'>"


class CropVariety(db.Model):
    """Specific cultivar or hybrid variety of a crop species."""
    __tablename__ = 'crop_varieties'

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='CASCADE'), nullable=False)
    variety_name = db.Column(db.String(100), nullable=False)
    maturity_type = db.Column(db.String(50), default='Medium Duration') # Early, Medium, Late
    disease_resistance = db.Column(db.String(255), default='Moderate')
    yield_potential_multiplier = db.Column(db.Float, default=1.1)

    def to_dict(self):
        return {
            'id': self.id,
            'crop_id': self.crop_id,
            'variety_name': self.variety_name,
            'maturity_type': self.maturity_type,
            'disease_resistance': self.disease_resistance,
            'yield_potential_multiplier': self.yield_potential_multiplier
        }


class CropCycle(db.Model):
    """Active or past crop growth cycle on a field plot."""
    __tablename__ = 'crop_cycles'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False, index=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='RESTRICT'), nullable=False, index=True)
    variety_id = db.Column(db.Integer, db.ForeignKey('crop_varieties.id', ondelete='SET NULL'), nullable=True)
    sowing_date = db.Column(db.Date, nullable=False)
    expected_harvest_date = db.Column(db.Date, nullable=False)
    actual_harvest_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='Growing', index=True) # Sown, Growing, Flowering, Harvesting, Completed, Failed
    acreage = db.Column(db.Float, default=1.0)
    seeding_rate_kg_per_acre = db.Column(db.Float, default=25.0)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    irrigation_schedules = db.relationship('IrrigationSchedule', backref='crop_cycle', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else 'Unknown',
            'variety_id': self.variety_id,
            'sowing_date': self.sowing_date.strftime('%Y-%m-%d') if self.sowing_date else None,
            'expected_harvest_date': self.expected_harvest_date.strftime('%Y-%m-%d') if self.expected_harvest_date else None,
            'actual_harvest_date': self.actual_harvest_date.strftime('%Y-%m-%d') if self.actual_harvest_date else None,
            'status': self.status,
            'acreage': self.acreage,
            'seeding_rate_kg_per_acre': self.seeding_rate_kg_per_acre,
            'notes': self.notes
        }

    def __repr__(self):
        return f"<CropCycle id={self.id} crop_id={self.crop_id} status='{self.status}'>"


class CropCompatibility(db.Model):
    """Crop rotation & companion planting compatibility rules."""
    __tablename__ = 'crop_compatibilities'

    id = db.Column(db.Integer, primary_key=True)
    crop_a_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='CASCADE'), nullable=False)
    crop_b_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='CASCADE'), nullable=False)
    relationship_type = db.Column(db.String(50), default='Rotation Friendly') # Rotation Friendly, Companion, Incompatible
    compatibility_score = db.Column(db.Float, default=85.0)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'crop_a_id': self.crop_a_id,
            'crop_b_id': self.crop_b_id,
            'relationship_type': self.relationship_type,
            'compatibility_score': self.compatibility_score,
            'notes': self.notes
        }


class CropPestDisease(db.Model):
    """Pests and diseases associated with specific crop species."""
    __tablename__ = 'crop_pest_diseases'

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    threat_level = db.Column(db.String(30), default='Moderate') # Mild, Moderate, High
    control_strategy = db.Column(db.Text, nullable=True)

    crop = db.relationship('Crop', backref=db.backref('pests_diseases', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'crop_id': self.crop_id,
            'name': self.name,
            'threat_level': self.threat_level,
            'control_strategy': self.control_strategy
        }


class CropGrowthStage(db.Model):
    """Agronomic growth stages (Germination, Vegetative, Flowering, Ripening)."""
    __tablename__ = 'crop_growth_stages'

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='CASCADE'), nullable=False)
    stage_name = db.Column(db.String(50), nullable=False) # Germination, Vegetative, Flowering, Yield Formation, Ripening
    start_day = db.Column(db.Integer, default=1)
    end_day = db.Column(db.Integer, default=20)
    kc_water_coefficient = db.Column(db.Float, default=1.0)

    crop = db.relationship('Crop', backref=db.backref('growth_stages', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'crop_id': self.crop_id,
            'stage_name': self.stage_name,
            'start_day': self.start_day,
            'end_day': self.end_day,
            'kc_water_coefficient': self.kc_water_coefficient
        }

