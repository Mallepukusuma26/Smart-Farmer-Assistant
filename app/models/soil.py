from datetime import datetime
from app.extensions import db

class SoilRecord(db.Model):
    """Soil test analysis record for a specific field plot."""
    __tablename__ = 'soil_records'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False, index=True)
    ph = db.Column(db.Float, nullable=False, default=6.5)
    nitrogen = db.Column(db.Float, nullable=False, default=140.0)      # N in mg/kg
    phosphorus = db.Column(db.Float, nullable=False, default=50.0)     # P in mg/kg
    potassium = db.Column(db.Float, nullable=False, default=200.0)     # K in mg/kg
    moisture = db.Column(db.Float, nullable=False, default=25.0)       # % moisture
    organic_carbon = db.Column(db.Float, nullable=False, default=0.75) # % OC
    electrical_conductivity = db.Column(db.Float, default=0.5)        # EC in dS/m
    cation_exchange_capacity = db.Column(db.Float, default=15.0)      # CEC meq/100g
    sulfur = db.Column(db.Float, default=12.0)                          # S in mg/kg
    zinc = db.Column(db.Float, default=1.5)                            # Zn in mg/kg
    iron = db.Column(db.Float, default=4.5)                            # Fe in mg/kg
    manganese = db.Column(db.Float, default=2.0)                       # Mn in mg/kg
    boron = db.Column(db.Float, default=0.5)                           # B in mg/kg
    soil_type = db.Column(db.String(50), nullable=False, default='Loamy')
    health_score = db.Column(db.Float, default=75.0)                  # Overall Soil Health Score (0-100)
    deficiency_summary = db.Column(db.Text, nullable=True)
    recommendation_notes = db.Column(db.Text, nullable=True)
    test_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    improvement_plans = db.relationship('SoilImprovementPlan', backref='soil_record', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'ph': self.ph,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'moisture': self.moisture,
            'organic_carbon': self.organic_carbon,
            'electrical_conductivity': self.electrical_conductivity,
            'cation_exchange_capacity': self.cation_exchange_capacity,
            'sulfur': self.sulfur,
            'zinc': self.zinc,
            'iron': self.iron,
            'manganese': self.manganese,
            'boron': self.boron,
            'soil_type': self.soil_type,
            'health_score': self.health_score,
            'deficiency_summary': self.deficiency_summary,
            'recommendation_notes': self.recommendation_notes,
            'test_date': self.test_date.strftime('%Y-%m-%d') if self.test_date else None
        }

    def __repr__(self):
        return f"<SoilRecord id={self.id} field_id={self.field_id} health_score={self.health_score}>"


class SoilSample(db.Model):
    """Raw physical soil sample collected from field grid points."""
    __tablename__ = 'soil_samples'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    sample_code = db.Column(db.String(50), unique=True, nullable=False)
    sampling_depth_cm = db.Column(db.Float, default=15.0)  # 0-15cm, 15-30cm
    sample_latitude = db.Column(db.Float, nullable=True)
    sample_longitude = db.Column(db.Float, nullable=True)
    collection_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    lab_name = db.Column(db.String(100), default='Local Agronomy Lab')
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'sample_code': self.sample_code,
            'sampling_depth_cm': self.sampling_depth_cm,
            'collection_date': self.collection_date.strftime('%Y-%m-%d')
        }


class SoilImprovementPlan(db.Model):
    """Actionable soil amendment plan derived from soil testing."""
    __tablename__ = 'soil_improvement_plans'

    id = db.Column(db.Integer, primary_key=True)
    soil_record_id = db.Column(db.Integer, db.ForeignKey('soil_records.id', ondelete='CASCADE'), nullable=False)
    amendment_type = db.Column(db.String(100), nullable=False)  # Lime, Gypsum, Organic Compost, Biochar
    target_parameter = db.Column(db.String(50), nullable=False) # pH, Nitrogen, Organic Matter
    recommended_dose_kg_per_acre = db.Column(db.Float, nullable=False)
    estimated_cost = db.Column(db.Float, default=0.0)
    timeframe_days = db.Column(db.Integer, default=30)
    status = db.Column(db.String(30), default='Planned') # Planned, Applied, Verified
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'soil_record_id': self.soil_record_id,
            'amendment_type': self.amendment_type,
            'target_parameter': self.target_parameter,
            'recommended_dose_kg_per_acre': self.recommended_dose_kg_per_acre,
            'estimated_cost': self.estimated_cost,
            'timeframe_days': self.timeframe_days,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class SoilNutrientTrend(db.Model):
    """Aggregate trend statistics for NPK and pH over multiple years."""
    __tablename__ = 'soil_nutrient_trends'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    year = db.Column(db.Integer, nullable=False, default=2026)
    avg_ph = db.Column(db.Float, default=6.5)
    avg_nitrogen = db.Column(db.Float, default=140.0)
    avg_phosphorus = db.Column(db.Float, default=50.0)
    avg_potassium = db.Column(db.Float, default=200.0)

    field = db.relationship('Field', backref=db.backref('nutrient_trends', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'year': self.year,
            'avg_ph': self.avg_ph,
            'avg_nitrogen': self.avg_nitrogen,
            'avg_phosphorus': self.avg_phosphorus,
            'avg_potassium': self.avg_potassium
        }


class SoilTestLab(db.Model):
    """Certified soil testing laboratory directory."""
    __tablename__ = 'soil_test_labs'

    id = db.Column(db.Integer, primary_key=True)
    lab_name = db.Column(db.String(150), nullable=False)
    accreditation_number = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'lab_name': self.lab_name,
            'accreditation_number': self.accreditation_number,
            'contact_phone': self.contact_phone,
            'address': self.address
        }

