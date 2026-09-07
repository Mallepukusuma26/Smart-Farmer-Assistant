import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.disease import Disease, DiseaseDetection
from ml.prediction.disease_predictor import DiseasePredictor

class DiseaseService:
    """Service layer for leaf image disease detection."""

    predictor = DiseasePredictor()

    @staticmethod
    def process_and_diagnose(farmer_id, image_file, field_id=None, upload_folder='uploads'):
        """Save uploaded leaf image, run offline ML diagnosis, and persist detection record."""
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(f"leaf_{farmer_id}_{int(datetime.utcnow().timestamp())}_{image_file.filename}")
        filepath = os.path.join(upload_folder, filename)
        image_file.save(filepath)

        diagnosis = DiseaseService.predictor.predict(filepath)

        detection = DiseaseDetection(
            field_id=field_id,
            farmer_id=farmer_id,
            image_filename=filename,
            detected_disease=diagnosis['disease_name'],
            confidence_score=diagnosis['confidence_score'],
            symptoms_observed=diagnosis['symptoms'],
            treatment_plan=f"Organic: {diagnosis['organic_treatment']} | Chemical: {diagnosis['chemical_treatment']}",
            status='Diagnosed'
        )

        db.session.add(detection)
        db.session.commit()
        return detection
