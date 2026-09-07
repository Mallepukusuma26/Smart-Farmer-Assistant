from app.extensions import db
from app.models.crop import Crop
from ml.prediction.crop_predictor import CropPredictor

class CropService:
    """Service layer for crop selection and ML crop recommendation."""
    
    predictor = CropPredictor()

    @staticmethod
    def recommend_crops(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
        """Invoke local ML CropPredictor model for top crop recommendations."""
        recommendations = CropService.predictor.predict(
            n=float(nitrogen),
            p=float(phosphorus),
            k=float(potassium),
            temperature=float(temperature),
            humidity=float(humidity),
            ph=float(ph),
            rainfall=float(rainfall)
        )

        # Enrich recommendations with database catalog parameters if available
        enriched = []
        for rec in recommendations:
            crop_obj = Crop.query.filter_by(name=rec['crop_name']).first()
            if crop_obj:
                rec['category'] = crop_obj.category
                rec['season'] = crop_obj.season
                rec['duration_days'] = crop_obj.duration_days
                rec['base_yield_per_acre'] = crop_obj.base_yield_per_acre
                rec['water_req_mm'] = crop_obj.water_req_mm
            else:
                rec['category'] = 'General Crop'
                rec['season'] = 'Kharif / Rabi'
                rec['duration_days'] = 120
                rec['base_yield_per_acre'] = 2.5
                rec['water_req_mm'] = 500.0

            enriched.append(rec)

        return enriched

    @staticmethod
    def get_all_crops():
        return Crop.query.order_by(Crop.name.asc()).all()
