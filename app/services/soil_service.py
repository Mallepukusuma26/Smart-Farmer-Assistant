from datetime import datetime
from app.extensions import db
from app.models.soil import SoilRecord
from ml.feature_engineering.feature_builder import compute_soil_health_score

class SoilService:
    """Service for soil testing analysis and health scoring."""

    @staticmethod
    def analyze_and_save_soil(field_id, ph, nitrogen, phosphorus, potassium, moisture=25.0, organic_carbon=0.75, electrical_conductivity=0.5, soil_type='Loamy'):
        """Analyze soil parameters, calculate health score, detect deficiencies, and save record."""
        health_score = compute_soil_health_score(ph, nitrogen, phosphorus, potassium, organic_carbon, electrical_conductivity)

        deficiencies = []
        recommendations = []

        if ph < 6.0:
            deficiencies.append("Acidic Soil (pH < 6.0)")
            recommendations.append("Apply Agricultural Lime (Calcium Carbonate) at 200 kg/acre to raise pH.")
        elif ph > 7.5:
            deficiencies.append("Alkaline Soil (pH > 7.5)")
            recommendations.append("Apply Gypsum or Elemental Sulfur at 150 kg/acre to reduce soil pH.")

        if nitrogen < 100:
            deficiencies.append("Nitrogen Deficiency (< 100 mg/kg)")
            recommendations.append("Apply Nitrogen-rich fertilizers like Urea or Neem Cake.")

        if phosphorus < 30:
            deficiencies.append("Phosphorus Deficiency (< 30 mg/kg)")
            recommendations.append("Apply Di-Ammonium Phosphate (DAP) or Single Super Phosphate (SSP).")

        if potassium < 120:
            deficiencies.append("Potassium Deficiency (< 120 mg/kg)")
            recommendations.append("Apply Muriate of Potash (MOP / KCl).")

        if organic_carbon < 0.5:
            deficiencies.append("Low Organic Matter (< 0.5% Organic Carbon)")
            recommendations.append("Incorporate Farmyard Manure (FYM) or green compost into soil before sowing.")

        deficiency_str = "; ".join(deficiencies) if deficiencies else "No major nutrient deficiencies detected."
        rec_str = "; ".join(recommendations) if recommendations else "Soil nutrient levels are well balanced."

        soil_record = SoilRecord(
            field_id=field_id,
            ph=float(ph),
            nitrogen=float(nitrogen),
            phosphorus=float(phosphorus),
            potassium=float(potassium),
            moisture=float(moisture),
            organic_carbon=float(organic_carbon),
            electrical_conductivity=float(electrical_conductivity),
            soil_type=soil_type,
            health_score=health_score,
            deficiency_summary=deficiency_str,
            recommendation_notes=rec_str,
            test_date=datetime.utcnow()
        )

        db.session.add(soil_record)
        db.session.commit()
        return soil_record
