from app.extensions import db
from app.models.fertilizer import Fertilizer, FertilizerRecommendation
from app.models.crop import Crop
from app.models.soil import SoilRecord

class FertilizerService:
    """Service layer for fertilizer deficit estimation and dosage recommendation engine."""

    @staticmethod
    def calculate_recommendation(field_id, crop_id, soil_record_id, area_acres=1.0, growth_stage='Basal'):
        """Calculate exact fertilizer requirements based on crop demand vs current soil NPK."""
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

        # Select suitable fertilizer combination
        rec_name = "NPK 19-19-19"
        qty_per_acre = 50.0

        if n_deficit > p_deficit and n_deficit > k_deficit:
            rec_name = "Urea (46% N)"
            qty_per_acre = (n_deficit / 0.46)
        elif p_deficit > n_deficit and p_deficit > k_deficit:
            rec_name = "DAP (18% N, 46% P2O5)"
            qty_per_acre = (p_deficit / 0.46)
        elif k_deficit > 0:
            rec_name = "Muriate of Potash - MOP (60% K2O)"
            qty_per_acre = (k_deficit / 0.60)

        qty_per_acre = round(max(20.0, min(qty_per_acre, 150.0)), 1)
        total_qty = round(qty_per_acre * float(area_acres), 1)

        fert_obj = Fertilizer.query.filter(Fertilizer.name.like(f"%{rec_name.split()[0]}%")).first()
        price_per_kg = fert_obj.price_per_kg if fert_obj else 25.0
        cost_estimate = round(total_qty * price_per_kg, 2)

        safety_notes = "Apply during morning or early evening hours. Ensure adequate soil moisture after application to prevent root burn."

        rec = FertilizerRecommendation(
            field_id=field_id,
            crop_id=crop_id,
            soil_record_id=soil_record_id,
            recommended_fertilizer=rec_name,
            quantity_kg_per_acre=qty_per_acre,
            total_quantity_kg=total_qty,
            application_stage=growth_stage,
            cost_estimate=cost_estimate,
            safety_notes=safety_notes
        )

        db.session.add(rec)
        db.session.commit()
        return rec
