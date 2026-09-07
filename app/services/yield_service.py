import json
from app.extensions import db
from app.models.yield_prediction import YieldPrediction
from app.models.crop import Crop
from app.models.field import Field
from ml.prediction.yield_predictor import YieldPredictor

class YieldService:
    """Service layer for crop yield regression inference."""

    predictor = YieldPredictor()

    @staticmethod
    def predict_yield(field_id, crop_id, nitrogen=100.0, phosphorus=40.0, potassium=120.0, ph=6.5, temperature=28.0, rainfall=800.0, irrigation_liters=50000.0, fertilizer_kg=100.0):
        """Invoke ML YieldPredictor regressor and save prediction."""
        field = Field.query.get(field_id)
        crop = Crop.query.get(crop_id)

        crop_name = crop.name if crop else 'Rice'
        soil_type = field.soil_type if field else 'Loamy'
        area = field.area if field else 1.0

        res = YieldService.predictor.predict(
            crop=crop_name,
            soil_type=soil_type,
            area_acres=area,
            nitrogen=float(nitrogen),
            phosphorus=float(phosphorus),
            potassium=float(potassium),
            ph=float(ph),
            temperature=float(temperature),
            rainfall=float(rainfall),
            irrigation_liters=float(irrigation_liters),
            fertilizer_kg=float(fertilizer_kg)
        )

        params_json = json.dumps({
            'crop': crop_name,
            'soil_type': soil_type,
            'area_acres': area,
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'ph': ph,
            'temperature': temperature,
            'rainfall': rainfall
        })

        prediction = YieldPrediction(
            field_id=field_id,
            crop_id=crop_id,
            predicted_yield_tons=res['predicted_yield_tons'],
            expected_range_min=res['expected_range_min'],
            expected_range_max=res['expected_range_max'],
            confidence_score=res['confidence_score'],
            parameters_json=params_json
        )

        db.session.add(prediction)
        db.session.commit()
        return prediction
