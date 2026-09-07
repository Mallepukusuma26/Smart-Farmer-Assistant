from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.disease import Disease, DiseaseSymptom, DiseaseTreatment, DiseaseDetection, DiseaseFeatureVector, DiseaseOutbreakAlert
from app.repositories.base_repository import BaseRepository

class DiseaseRepository(BaseRepository[DiseaseDetection]):
    """Data Access Repository for Crop Diseases, Image Diagnostic Logs, Feature Vectors, and Outbreak Warnings."""

    def __init__(self):
        super().__init__(DiseaseDetection)

    def find_disease_by_name(self, name: str) -> Optional[Disease]:
        """Look up catalog disease entry by name."""
        return db.session.query(Disease).filter(func.lower(Disease.name) == name.lower().strip()).first()

    def get_diseases_by_crop(self, crop_name: str) -> List[Disease]:
        """Fetch diseases affecting a specific crop species."""
        return db.session.query(Disease).filter(
            or_(func.lower(Disease.crop_name) == crop_name.lower().strip(), Disease.crop_name == 'All Crops')
        ).all()

    def search_disease_catalog(self, keyword: Optional[str] = None, crop_name: Optional[str] = None, cause: Optional[str] = None) -> List[Disease]:
        """Search disease catalog by symptoms, treatment, or pathogen cause."""
        query = db.session.query(Disease)
        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(
                or_(
                    Disease.name.ilike(term),
                    Disease.symptoms.ilike(term),
                    Disease.prevention.ilike(term),
                    Disease.organic_treatment.ilike(term),
                    Disease.chemical_treatment.ilike(term)
                )
            )
        if crop_name:
            query = query.filter(or_(Disease.crop_name == crop_name, Disease.crop_name == 'All Crops'))
        if cause:
            query = query.filter(Disease.cause == cause)
        return query.order_by(Disease.name.asc()).all()

    def save_detection(self, farmer_id: int, image_filename: str, detected_disease: str, confidence_score: float, field_id: Optional[int] = None, disease_id: Optional[int] = None, severity_estimated: str = 'Moderate', affected_area_pct: float = 15.0, symptoms_observed: Optional[str] = None, treatment_plan: Optional[str] = None, image_path: Optional[str] = None) -> DiseaseDetection:
        """Save leaf diagnostic image inference record."""
        detection = DiseaseDetection(
            farmer_id=farmer_id,
            field_id=field_id,
            disease_id=disease_id,
            image_filename=image_filename,
            image_path=image_path,
            detected_disease=detected_disease,
            confidence_score=confidence_score,
            severity_estimated=severity_estimated,
            affected_area_pct=affected_area_pct,
            symptoms_observed=symptoms_observed,
            treatment_plan=treatment_plan,
            status='Diagnosed'
        )
        db.session.add(detection)
        db.session.commit()
        return detection

    def get_farmer_detections(self, farmer_id: int, limit: Optional[int] = None) -> List[DiseaseDetection]:
        """Fetch diagnostic history logs for a farmer."""
        query = db.session.query(DiseaseDetection).filter_by(farmer_id=farmer_id).order_by(DiseaseDetection.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def save_feature_vector(self, detection_id: int, mean_hue: float, mean_saturation: float, mean_value: float, green_red_ratio: float, texture_contrast: float, texture_homogeneity: float, lesion_count: int = 0) -> DiseaseFeatureVector:
        """Save OpenCV extracted color/texture features for audit."""
        fv = DiseaseFeatureVector(
            detection_id=detection_id,
            mean_hue=mean_hue,
            mean_saturation=mean_saturation,
            mean_value=mean_value,
            green_red_ratio=green_red_ratio,
            texture_contrast=texture_contrast,
            texture_homogeneity=texture_homogeneity,
            lesion_count=lesion_count
        )
        db.session.add(fv)
        db.session.commit()
        return fv

    def get_outbreak_alerts(self, crop_name: Optional[str] = None, region: Optional[str] = None) -> List[DiseaseOutbreakAlert]:
        """Fetch active regional disease outbreak alerts."""
        query = db.session.query(DiseaseOutbreakAlert).filter_by(is_active=True)
        if crop_name:
            query = query.filter_by(crop_name=crop_name)
        if region:
            query = query.filter_by(region_location=region)
        return query.order_by(DiseaseOutbreakAlert.issued_at.desc()).all()
