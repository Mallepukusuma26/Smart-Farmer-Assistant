from datetime import datetime
from app.extensions import db

class SoilRecord(db.Model):
    """Soil test analysis record for a specific field."""
    __tablename__ = 'soil_records'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    ph = db.Column(db.Float, nullable=False, default=6.5)
    nitrogen = db.Column(db.Float, nullable=False, default=140.0)      # N in mg/kg or kg/ha
    phosphorus = db.Column(db.Float, nullable=False, default=50.0)     # P in mg/kg or kg/ha
    potassium = db.Column(db.Float, nullable=False, default=200.0)     # K in mg/kg or kg/ha
    moisture = db.Column(db.Float, nullable=False, default=25.0)       # % moisture
    organic_carbon = db.Column(db.Float, nullable=False, default=0.75) # % OC
    electrical_conductivity = db.Column(db.Float, default=0.5)        # EC in dS/m
    soil_type = db.Column(db.String(50), nullable=False, default='Loamy')
    health_score = db.Column(db.Float, default=75.0)                  # Overall Soil Health Score (0-100)
    deficiency_summary = db.Column(db.Text, nullable=True)
    recommendation_notes = db.Column(db.Text, nullable=True)
    test_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

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
            'soil_type': self.soil_type,
            'health_score': self.health_score,
            'deficiency_summary': self.deficiency_summary,
            'recommendation_notes': self.recommendation_notes,
            'test_date': self.test_date.strftime('%Y-%m-%d') if self.test_date else None
        }

    def __repr__(self):
        return f"<SoilRecord id={self.id} field_id={self.field_id} health_score={self.health_score}>"
