from datetime import datetime
from typing import Dict, Any, List, Optional
from app.extensions import db

class Disease(db.Model):
    """Catalog of crop leaf diseases and management guidelines."""
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(150), nullable=True)
    cause = db.Column(db.String(255), nullable=True) # Fungal, Bacterial, Viral, Nutrient Deficiency, Pest
    severity_level = db.Column(db.String(30), default='Moderate') # Low, Moderate, Severe, Destructive
    favorable_humidity_pct = db.Column(db.Float, nullable=True, default=75.0)
    favorable_temp_c = db.Column(db.Float, nullable=True, default=26.0)
    symptoms = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text, nullable=True)
    organic_treatment = db.Column(db.Text, nullable=True)
    chemical_treatment = db.Column(db.Text, nullable=True)
    image_sample_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    detections = db.relationship('DiseaseDetection', backref='disease_ref', lazy='dynamic')
    symptom_catalog = db.relationship('DiseaseSymptom', backref='disease', lazy='dynamic', cascade='all, delete-orphan')
    treatment_catalog = db.relationship('DiseaseTreatment', backref='disease', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'crop_name': self.crop_name,
            'scientific_name': self.scientific_name,
            'cause': self.cause,
            'severity_level': self.severity_level,
            'favorable_humidity_pct': self.favorable_humidity_pct,
            'favorable_temp_c': self.favorable_temp_c,
            'symptoms': self.symptoms,
            'prevention': self.prevention,
            'organic_treatment': self.organic_treatment,
            'chemical_treatment': self.chemical_treatment,
            'image_sample_path': self.image_sample_path,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self) -> str:
        return f"<Disease id={self.id} name='{self.name}' crop='{self.crop_name}'>"


class DiseaseSymptom(db.Model):
    """Detailed visual symptom markers for leaf disease identification."""
    __tablename__ = 'disease_symptoms'

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id', ondelete='CASCADE'), nullable=False)
    body_part = db.Column(db.String(50), default='Leaf') # Leaf, Stem, Fruit, Root, Flower
    symptom_pattern = db.Column(db.String(100), nullable=False) # Yellow spots, Brown lesions, Powdery coating, Blight
    color_hue_range = db.Column(db.String(50), nullable=True) # Yellowish-brown, Dark brown, White
    typical_stage = db.Column(db.String(50), default='Early') # Early, Intermediate, Advanced

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'disease_id': self.disease_id,
            'body_part': self.body_part,
            'symptom_pattern': self.symptom_pattern,
            'color_hue_range': self.color_hue_range,
            'typical_stage': self.typical_stage
        }


class DiseaseTreatment(db.Model):
    """Actionable curative and biological remedy prescriptions."""
    __tablename__ = 'disease_treatments'

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id', ondelete='CASCADE'), nullable=False)
    treatment_type = db.Column(db.String(50), nullable=False, default='Chemical') # Chemical, Organic, Cultural, Biological
    title = db.Column(db.String(150), nullable=False)
    product_active_ingredient = db.Column(db.String(150), nullable=True)
    dosage_per_acre = db.Column(db.String(100), nullable=False, default='250 ml / 100L water')
    application_instructions = db.Column(db.Text, nullable=False)
    safety_precautions = db.Column(db.Text, nullable=True)
    estimated_cost_per_acre = db.Column(db.Float, default=0.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'disease_id': self.disease_id,
            'treatment_type': self.treatment_type,
            'title': self.title,
            'product_active_ingredient': self.product_active_ingredient,
            'dosage_per_acre': self.dosage_per_acre,
            'application_instructions': self.application_instructions,
            'safety_precautions': self.safety_precautions,
            'estimated_cost_per_acre': self.estimated_cost_per_acre
        }


class DiseaseDetection(db.Model):
    """Diagnostic log of farmer leaf image uploads and local model predictions."""
    __tablename__ = 'disease_detections'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id', ondelete='SET NULL'), nullable=True)
    image_filename = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    detected_disease = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False, default=0.0) # 0.0 - 1.0 (e.g. 0.94 -> 94%)
    severity_estimated = db.Column(db.String(30), default='Moderate') # Mild, Moderate, Severe
    affected_area_pct = db.Column(db.Float, default=15.0)
    symptoms_observed = db.Column(db.Text, nullable=True)
    treatment_plan = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Diagnosed') # Diagnosed, Under Treatment, Resolved, Ignored
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def update_status(self, new_status: str, notes: Optional[str] = None) -> None:
        """Transition diagnostic case status."""
        self.status = new_status
        if notes:
            self.symptoms_observed = f"{self.symptoms_observed or ''}\n[Update]: {notes}".strip()

    def is_high_confidence(self) -> bool:
        """Check if confidence score exceeds minimum reliability threshold of 75%."""
        return self.confidence_score >= 0.75

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'farmer_id': self.farmer_id,
            'disease_id': self.disease_id,
            'image_filename': self.image_filename,
            'image_path': self.image_path,
            'detected_disease': self.detected_disease,
            'confidence_score': round(self.confidence_score * 100, 1),
            'severity_estimated': self.severity_estimated,
            'affected_area_pct': self.affected_area_pct,
            'symptoms_observed': self.symptoms_observed,
            'treatment_plan': self.treatment_plan,
            'status': self.status,
            'is_high_confidence': self.is_high_confidence(),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<DiseaseDetection id={self.id} disease='{self.detected_disease}' confidence={self.confidence_score}>"


class DiseaseFeatureVector(db.Model):
    """Extracted OpenCV color/texture feature vectors stored for local classifier audit."""
    __tablename__ = 'disease_feature_vectors'

    id = db.Column(db.Integer, primary_key=True)
    detection_id = db.Column(db.Integer, db.ForeignKey('disease_detections.id', ondelete='CASCADE'), nullable=False)
    mean_hue = db.Column(db.Float, nullable=False, default=0.0)
    mean_saturation = db.Column(db.Float, nullable=False, default=0.0)
    mean_value = db.Column(db.Float, nullable=False, default=0.0)
    green_red_ratio = db.Column(db.Float, nullable=False, default=1.0)
    texture_contrast = db.Column(db.Float, nullable=False, default=0.0)
    texture_homogeneity = db.Column(db.Float, nullable=False, default=0.0)
    lesion_count = db.Column(db.Integer, default=0)
    extracted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    detection = db.relationship('DiseaseDetection', backref=db.backref('feature_vector', uselist=False, cascade='all, delete-orphan'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'detection_id': self.detection_id,
            'mean_hue': self.mean_hue,
            'mean_saturation': self.mean_saturation,
            'mean_value': self.mean_value,
            'green_red_ratio': self.green_red_ratio,
            'texture_contrast': self.texture_contrast,
            'texture_homogeneity': self.texture_homogeneity,
            'lesion_count': self.lesion_count,
            'extracted_at': self.extracted_at.strftime('%Y-%m-%d %H:%M')
        }


class DiseaseOutbreakAlert(db.Model):
    """Regional outbreak warning alerts triggered by spatial cluster detection."""
    __tablename__ = 'disease_outbreak_alerts'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    disease_name = db.Column(db.String(100), nullable=False)
    region_location = db.Column(db.String(150), nullable=False)
    cluster_cases_count = db.Column(db.Integer, default=1)
    risk_level = db.Column(db.String(20), default='High') # Medium, High, Emergency
    advisory_notice = db.Column(db.Text, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'disease_name': self.disease_name,
            'region_location': self.region_location,
            'cluster_cases_count': self.cluster_cases_count,
            'risk_level': self.risk_level,
            'advisory_notice': self.advisory_notice,
            'issued_at': self.issued_at.strftime('%Y-%m-%d %H:%M'),
            'is_active': self.is_active
        }

