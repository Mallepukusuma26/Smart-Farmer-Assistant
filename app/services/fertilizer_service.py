from typing import Dict, Any, List, Optional
from app.repositories.fertilizer_repository import FertilizerRepository
from app.models.fertilizer import Fertilizer, FertilizerRecommendation
from app.models.crop import Crop
from app.models.soil import SoilRecord

class FertilizerService:
    """Domain Service for NPK deficit calculations, dosage recommendation, cost estimation, and split scheduling."""

    def __init__(self, repository: Optional[FertilizerRepository] = None):
        self.repository = repository or FertilizerRepository()

    def convert_area(self, area: float, from_unit: str = 'Acres', to_unit: str = 'Hectares') -> float:
        """Convert land area between Acres, Hectares, and Square Meters."""
        if from_unit == to_unit:
            return area
        # Base unit: Acres
        acres = area
        if from_unit == 'Hectares':
            acres = area * 2.47105
        elif from_unit == 'SqMeters':
            acres = area * 0.000247105

        if to_unit == 'Acres':
            return round(acres, 2)
        elif to_unit == 'Hectares':
            return round(acres / 2.47105, 2)
        elif to_unit == 'SqMeters':
            return round(acres * 4046.86, 1)
        return area

    def calculate_recommendation(
        self,
        field_id: int,
        crop_id: int,
        soil_record_id: Optional[int] = None,
        area_acres: float = 1.0,
        growth_stage: str = 'Basal'
    ) -> FertilizerRecommendation:
        """Calculate exact NPK nutrient deficit and generate dosage recommendations."""
        crop = Crop.query.get(crop_id)
        soil = SoilRecord.query.get(soil_record_id) if soil_record_id else None

        current_n = soil.nitrogen if soil else 100.0
        current_p = soil.phosphorus if soil else 40.0
        current_k = soil.potassium if soil else 120.0

        target_n = crop.min_n if crop else 120.0
        target_p = crop.min_p if crop else 60.0
        target_k = crop.min_k if crop else 60.0

        n_deficit = max(0.0, target_n - current_n)
        p_deficit = max(0.0, target_p - current_p)
        k_deficit = max(0.0, target_k - current_k)

        # Select primary fertilizer recommendation product
        rec_name = "NPK 19-19-19"
        qty_per_acre = 50.0

        if n_deficit >= p_deficit and n_deficit >= k_deficit and n_deficit > 0:
            rec_name = "Urea (46% N)"
            qty_per_acre = (n_deficit / 0.46)
        elif p_deficit >= n_deficit and p_deficit >= k_deficit and p_deficit > 0:
            rec_name = "DAP (18% N, 46% P2O5)"
            qty_per_acre = (p_deficit / 0.46)
        elif k_deficit > 0:
            rec_name = "Muriate of Potash (MOP 60% K2O)"
            qty_per_acre = (k_deficit / 0.60)

        qty_per_acre = round(max(15.0, min(qty_per_acre, 160.0)), 1)
        total_qty = round(qty_per_acre * float(area_acres), 1)

        fert_obj = self.repository.find_by_name(rec_name)
        price_per_kg = fert_obj.price_per_kg if fert_obj else 28.0
        cost_estimate = round(total_qty * price_per_kg, 2)

        safety_notes = (
            "Apply during cool morning or evening hours to prevent volatization loss. "
            "Maintain proper soil moisture via irrigation following application to prevent root burn."
        )

        return self.repository.save_recommendation(
            field_id=field_id,
            recommended_fertilizer=rec_name,
            quantity_kg_per_acre=qty_per_acre,
            total_quantity_kg=total_qty,
            crop_id=crop_id,
            soil_record_id=soil_record_id,
            application_stage=growth_stage,
            cost_estimate=cost_estimate,
            safety_notes=safety_notes
        )

    def generate_split_application_schedule(self, total_nitrogen_kg: float) -> List[Dict[str, Any]]:
        """Generate 3-stage split application dosage schedule (Basal, Vegetative, Flowering)."""
        return [
            {
                'stage': 'Basal (At Sowing)',
                'nitrogen_pct': 50.0,
                'dosage_kg': round(total_nitrogen_kg * 0.50, 1),
                'method': 'Soil Incorporation'
            },
            {
                'stage': 'Vegetative (30 Days After Sowing)',
                'nitrogen_pct': 25.0,
                'dosage_kg': round(total_nitrogen_kg * 0.25, 1),
                'method': 'Side Dressing / Broadcasting'
            },
            {
                'stage': 'Flowering / Panicle (60 Days After Sowing)',
                'nitrogen_pct': 25.0,
                'dosage_kg': round(total_nitrogen_kg * 0.25, 1),
                'method': 'Foliar Spray or Fertigation'
            }
        ]
