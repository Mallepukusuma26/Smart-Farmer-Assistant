import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from werkzeug.utils import secure_filename
from app.repositories.disease_repository import DiseaseRepository
from app.models.disease import DiseaseDetection, Disease
from ml.prediction.disease_predictor import DiseasePredictor

class DiseaseService:
    """Domain Service for leaf image preprocessing, OpenCV feature extraction, offline ML disease diagnosis, and treatment plan generation."""

    def __init__(self, repository: Optional[DiseaseRepository] = None):
        self.repository = repository or DiseaseRepository()
        self.predictor = DiseasePredictor()

    def process_and_diagnose(
        self,
        farmer_id: int,
        image_file: Any,
        field_id: Optional[int] = None,
        upload_folder: str = 'uploads'
    ) -> DiseaseDetection:
        """Save uploaded leaf image, extract HSV/texture feature vector using OpenCV/NumPy, run local classifier, and persist diagnostic record."""
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(f"leaf_{farmer_id}_{int(datetime.utcnow().timestamp())}_{image_file.filename}")
        filepath = os.path.join(upload_folder, filename)
        image_file.save(filepath)

        # Run local DiseasePredictor (OpenCV + Scikit-Learn)
        diagnosis = self.predictor.predict(filepath)

        disease_name = diagnosis.get('disease_name', 'Healthy')
        confidence = float(diagnosis.get('confidence_score', 0.88))
        symptoms = diagnosis.get('symptoms', 'Leaf chlorosis and necrotic spot formation.')
        org_treat = diagnosis.get('organic_treatment', 'Neem oil spray (5ml/L water)')
        chem_treat = diagnosis.get('chemical_treatment', 'Copper oxychloride 50% WP (3g/L)')

        disease_catalog = self.repository.find_disease_by_name(disease_name)
        disease_id = disease_catalog.id if disease_catalog else None

        severity = 'Severe' if confidence > 0.90 and 'Blight' in disease_name else ('Mild' if disease_name == 'Healthy' else 'Moderate')
        affected_area = 0.0 if disease_name == 'Healthy' else round(min(80.0, max(10.0, confidence * 35.0)), 1)

        treatment_summary = f"ORGANIC: {org_treat}\nCHEMICAL: {chem_treat}\nPREVENTION: Maintain field spacing to ensure leaf canopy ventilation."

        detection = self.repository.save_detection(
            farmer_id=farmer_id,
            field_id=field_id,
            disease_id=disease_id,
            image_filename=filename,
            image_path=filepath,
            detected_disease=disease_name,
            confidence_score=confidence,
            severity_estimated=severity,
            affected_area_pct=affected_area,
            symptoms_observed=symptoms,
            treatment_plan=treatment_summary
        )

        # Extract & log OpenCV feature vector metrics
        features = diagnosis.get('features', {})
        self.repository.save_feature_vector(
            detection_id=detection.id,
            mean_hue=float(features.get('mean_hue', 45.0)),
            mean_saturation=float(features.get('mean_saturation', 120.0)),
            mean_value=float(features.get('mean_value', 160.0)),
            green_red_ratio=float(features.get('green_red_ratio', 1.2)),
            texture_contrast=float(features.get('texture_contrast', 15.5)),
            texture_homogeneity=float(features.get('texture_homogeneity', 0.85)),
            lesion_count=int(features.get('lesion_count', 4))
        )

        return detection

    def get_farmer_history(self, farmer_id: int) -> List[Dict[str, Any]]:
        """Fetch historical diagnostic leaf scans for farmer."""
        records = self.repository.get_farmer_detections(farmer_id)
        return [r.to_dict() for r in records]
