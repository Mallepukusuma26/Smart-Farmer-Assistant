from datetime import datetime
from app.extensions import db

class Disease(db.Model):
    """Catalog of crop leaf diseases and management guidelines."""
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    cause = db.Column(db.String(255), nullable=True) # Fungal, Bacterial, Viral, Nutrient Deficiency
    prevention = db.Column(db.Text, nullable=True)
    organic_treatment = db.Column(db.Text, nullable=True)
    chemical_treatment = db.Column(db.Text, nullable=True)
    image_sample_path = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'crop_name': self.crop_name,
            'symptoms': self.symptoms,
            'cause': self.cause,
            'prevention': self.prevention,
            'organic_treatment': self.organic_treatment,
            'chemical_treatment': self.chemical_treatment,
            'image_sample_path': self.image_sample_path
        }

    def __repr__(self):
        return f"<Disease id={self.id} name='{self.name}'>"


class DiseaseDetection(db.Model):
    """Diagnostic log of farmer leaf image uploads and model predictions."""
    __tablename__ = 'disease_detections'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    detected_disease = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False, default=0.0) # 0.0 - 1.0 (e.g. 0.94 -> 94%)
    symptoms_observed = db.Column(db.Text, nullable=True)
    treatment_plan = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Diagnosed') # Diagnosed, Under Treatment, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'farmer_id': self.farmer_id,
            'image_filename': self.image_filename,
            'detected_disease': self.detected_disease,
            'confidence_score': round(self.confidence_score * 100, 1),
            'symptoms_observed': self.symptoms_observed,
            'treatment_plan': self.treatment_plan,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self):
        return f"<DiseaseDetection id={self.id} disease='{self.detected_disease}' confidence={self.confidence_score}>"
