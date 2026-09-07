from typing import Dict, Any, List, Optional
from app.repositories.crop_repository import CropRepository
from app.models.crop import Crop
from ml.prediction.crop_predictor import CropPredictor

class CropService:
    """Domain Service for ML crop recommendation, rotation scoring, and species catalog management."""

    def __init__(self, repository: Optional[CropRepository] = None):
        self.repository = repository or CropRepository()
        self.predictor = CropPredictor()

    def recommend_crops(
        self,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """Invoke local ML multi-classifier model for top N crop recommendations enriched with catalog metadata."""
        predictions = self.predictor.predict(
            n=float(nitrogen),
            p=float(phosphorus),
            k=float(potassium),
            temperature=float(temperature),
            humidity=float(humidity),
            ph=float(ph),
            rainfall=float(rainfall)
        )

        results = []
        for rec in predictions[:top_n]:
            crop_name = rec['crop_name']
            crop_obj = self.repository.find_by_name(crop_name)

            item = {
                'crop_name': crop_name,
                'confidence_score': rec.get('confidence', 85.0),
                'match_rating': rec.get('match_rating', 'Highly Recommended')
            }

            if crop_obj:
                item['crop_id'] = crop_obj.id
                item['category'] = crop_obj.category
                item['season'] = crop_obj.season
                item['duration_days'] = crop_obj.duration_days
                item['base_yield_per_acre'] = crop_obj.base_yield_per_acre
                item['water_req_mm'] = crop_obj.water_req_mm
                item['ideal_soil_type'] = crop_obj.ideal_soil_type
                item['description'] = crop_obj.description
            else:
                item['crop_id'] = None
                item['category'] = 'General Crop'
                item['season'] = 'Kharif / Rabi'
                item['duration_days'] = 120
                item['base_yield_per_acre'] = 2.5
                item['water_req_mm'] = 500.0
                item['ideal_soil_type'] = 'Loamy'
                item['description'] = 'Agronomic crop species.'

            results.append(item)

        return results

    def evaluate_rotation(self, previous_crop_id: int, proposed_crop_id: int) -> Dict[str, Any]:
        """Evaluate crop rotation compatibility score between consecutive crop seasons."""
        score = self.repository.check_rotation_compatibility(previous_crop_id, proposed_crop_id)

        prev_crop = self.repository.get_by_id(previous_crop_id)
        prop_crop = self.repository.get_by_id(proposed_crop_id)

        prev_name = prev_crop.name if prev_crop else "Previous Crop"
        prop_name = prop_crop.name if prop_crop else "Proposed Crop"

        status = "Excellent Rotation" if score >= 85.0 else ("Acceptable Rotation" if score >= 65.0 else "Incompatible Rotation")

        notes = f"Rotating from {prev_name} to {prop_name} promotes nitrogen fixation and prevents soil pest buildup." if score >= 75.0 else f"Repeated planting of similar crop species may deplete specific soil nutrients."

        return {
            'previous_crop': prev_name,
            'proposed_crop': prop_name,
            'compatibility_score': score,
            'rotation_status': status,
            'agronomic_notes': notes
        }

    def get_all_crops(self) -> List[Crop]:
        """Fetch all catalog crop species ordered alphabetically."""
        return Crop.query.order_by(Crop.name.asc()).all()
