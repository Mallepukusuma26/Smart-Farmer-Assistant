from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from app.repositories.soil_repository import SoilRepository
from app.models.soil import SoilRecord, SoilImprovementPlan

class SoilService:
    """Domain Service for soil testing analysis, nutrient deficiency detection, health scoring, and amendment plans."""

    def __init__(self, repository: Optional[SoilRepository] = None):
        self.repository = repository or SoilRepository()

    def get_recent_samples_by_farmer(self, farmer_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch most recent soil test samples for a farmer's fields."""
        from app.models.field import Field
        from app.models.farm import Farm
        from app.extensions import db
        records = db.session.query(SoilRecord).join(Field, SoilRecord.field_id == Field.id).join(Farm, Field.farm_id == Farm.id).filter(Farm.farmer_id == farmer_id).order_by(SoilRecord.test_date.desc()).limit(limit).all()
        return [r.to_dict() for r in records]

    def calculate_health_score(self, ph: float, N: float, P: float, K: float, OC: float = 0.75, EC: float = 0.5) -> float:
        """Calculate weighted soil health score index (0-100%)."""
        score = 100.0

        # pH penalty (Optimal 6.0 - 7.5)
        if ph < 6.0:
            score -= (6.0 - ph) * 12.0
        elif ph > 7.5:
            score -= (ph - 7.5) * 12.0

        # Nitrogen penalty (Optimal 120 - 250 mg/kg)
        if N < 120:
            score -= min(25.0, (120 - N) * 0.2)
        elif N > 300:
            score -= min(15.0, (N - 300) * 0.1)

        # Phosphorus penalty (Optimal 40 - 100 mg/kg)
        if P < 40:
            score -= min(20.0, (40 - P) * 0.4)
        elif P > 120:
            score -= min(10.0, (P - 120) * 0.1)

        # Potassium penalty (Optimal 150 - 300 mg/kg)
        if K < 150:
            score -= min(20.0, (150 - K) * 0.15)
        elif K > 400:
            score -= min(10.0, (K - 400) * 0.05)

        # Organic Carbon bonus/penalty (Optimal > 0.75%)
        if OC < 0.5:
            score -= 15.0
        elif OC >= 1.0:
            score += 5.0

        # EC penalty (> 2.0 dS/m indicates salinity stress)
        if EC > 2.0:
            score -= min(25.0, (EC - 2.0) * 10.0)

        return round(max(10.0, min(100.0, score)), 1)

    @staticmethod
    def analyze_and_save_soil(
        field_id: int,
        ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        moisture: float = 25.0,
        organic_carbon: float = 0.75,
        electrical_conductivity: float = 0.5,
        soil_type: str = 'Loamy'
    ) -> SoilRecord:
        """Perform comprehensive agronomic soil analysis, detect deficiencies, create improvement plans, and persist record."""
        service = SoilService()
        health_score = service.calculate_health_score(ph, nitrogen, phosphorus, potassium, organic_carbon, electrical_conductivity)



        deficiencies: List[str] = []
        recommendations: List[str] = []
        plans: List[Dict[str, Any]] = []

        if ph < 6.0:
            deficiencies.append("Acidic Soil (pH < 6.0)")
            recommendations.append("Apply Agricultural Lime (Calcium Carbonate) at 200 kg/acre to raise pH.")
            plans.append({
                'amendment_type': 'Agricultural Lime',
                'target_parameter': 'pH',
                'recommended_dose_kg_per_acre': 200.0,
                'estimated_cost': 1200.0,
                'timeframe_days': 30
            })
        elif ph > 7.5:
            deficiencies.append("Alkaline Soil (pH > 7.5)")
            recommendations.append("Apply Gypsum or Elemental Sulfur at 150 kg/acre to reduce soil pH.")
            plans.append({
                'amendment_type': 'Agricultural Gypsum',
                'target_parameter': 'pH',
                'recommended_dose_kg_per_acre': 150.0,
                'estimated_cost': 950.0,
                'timeframe_days': 30
            })

        if nitrogen < 120:
            deficiencies.append("Nitrogen Deficiency (< 120 mg/kg)")
            recommendations.append("Apply Nitrogen-rich fertilizers like Urea (46% N) or Neem Cake.")
            plans.append({
                'amendment_type': 'Urea (46% N)',
                'target_parameter': 'Nitrogen',
                'recommended_dose_kg_per_acre': 50.0,
                'estimated_cost': 1100.0,
                'timeframe_days': 15
            })

        if phosphorus < 40:
            deficiencies.append("Phosphorus Deficiency (< 40 mg/kg)")
            recommendations.append("Apply Di-Ammonium Phosphate (DAP 18-46-0) or Single Super Phosphate.")
            plans.append({
                'amendment_type': 'DAP (18-46-0)',
                'target_parameter': 'Phosphorus',
                'recommended_dose_kg_per_acre': 40.0,
                'estimated_cost': 1400.0,
                'timeframe_days': 15
            })

        if potassium < 150:
            deficiencies.append("Potassium Deficiency (< 150 mg/kg)")
            recommendations.append("Apply Muriate of Potash (MOP 60% K2O).")
            plans.append({
                'amendment_type': 'MOP (60% K2O)',
                'target_parameter': 'Potassium',
                'recommended_dose_kg_per_acre': 30.0,
                'estimated_cost': 900.0,
                'timeframe_days': 15
            })

        if organic_carbon < 0.5:
            deficiencies.append("Low Organic Matter (< 0.5% Organic Carbon)")
            recommendations.append("Incorporate Farmyard Manure (FYM) or green leaf compost into soil.")
            plans.append({
                'amendment_type': 'Organic Farmyard Compost',
                'target_parameter': 'Organic Matter',
                'recommended_dose_kg_per_acre': 500.0,
                'estimated_cost': 2500.0,
                'timeframe_days': 45
            })

        deficiency_str = "; ".join(deficiencies) if deficiencies else "No major nutrient deficiencies detected."
        rec_str = "; ".join(recommendations) if recommendations else "Soil nutrient levels are well balanced."

        record = service.repository.create(
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

        for p in plans:
            service.repository.add_improvement_plan(
                soil_record_id=record.id,
                amendment_type=p['amendment_type'],
                target_parameter=p['target_parameter'],
                dose_kg_per_acre=p['recommended_dose_kg_per_acre'],
                estimated_cost=p['estimated_cost'],
                timeframe_days=p['timeframe_days']
            )

        return record


    def compare_soil_history(self, field_id: int) -> Dict[str, Any]:
        """Compare current soil test with previous historical soil test to evaluate improvement trend."""
        records = self.repository.get_records_by_field(field_id)
        if not records:
            return {'status': 'No soil records available.'}

        current = records[0]
        previous = records[1] if len(records) > 1 else None

        delta = {}
        if previous:
            delta = {
                'ph_change': round(current.ph - previous.ph, 2),
                'nitrogen_change': round(current.nitrogen - previous.nitrogen, 1),
                'phosphorus_change': round(current.phosphorus - previous.phosphorus, 1),
                'potassium_change': round(current.potassium - previous.potassium, 1),
                'health_score_change': round(current.health_score - previous.health_score, 1)
            }

        return {
            'current_record': current.to_dict(),
            'previous_record': previous.to_dict() if previous else None,
            'improvement_delta': delta,
            'total_test_count': len(records)
        }
