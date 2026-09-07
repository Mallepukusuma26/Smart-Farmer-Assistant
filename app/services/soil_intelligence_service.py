"""
Soil Intelligence Service Module for Smart Farmer Assistant.

Provides comprehensive soil chemical/physical evaluation, NPK nutrient balance indexing,
deficiency detection, soil amendment planning, and historical fertility trend tracking.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.extensions import db
from app.models.soil import SoilRecord
from app.repositories.soil_repository import SoilRepository


class SoilIntelligenceService:
    """
    Advanced Soil Intelligence engine for pH balancing, N-P-K nutrient status,
    organic carbon health scoring, and multi-test trend analysis.
    """

    def __init__(self, repository: Optional[SoilRepository] = None):
        self.repository = repository or SoilRepository()

    def evaluate_nutrient_balance(self, n: float, p: float, k: float) -> Dict[str, Any]:
        """
        Evaluates soil N-P-K concentrations against optimal agronomic targets.
        Target ranges (mg/kg or kg/ha equivalent):
        - Nitrogen (N): 140 - 250
        - Phosphorus (P): 45 - 90
        - Potassium (K): 150 - 300
        """
        n_status = "Optimal" if 140 <= n <= 250 else ("Deficient" if n < 140 else "Excessive")
        p_status = "Optimal" if 45 <= p <= 90 else ("Deficient" if p < 45 else "Excessive")
        k_status = "Optimal" if 150 <= k <= 300 else ("Deficient" if k < 150 else "Excessive")

        deficiencies = []
        if n_status == "Deficient":
            deficiencies.append("Nitrogen (N) deficiency detected — apply Urea or Ammonium Nitrate.")
        if p_status == "Deficient":
            deficiencies.append("Phosphorus (P) deficiency detected — apply Single Super Phosphate (SSP) or DAP.")
        if k_status == "Deficient":
            deficiencies.append("Potassium (K) deficiency detected — apply Muriate of Potash (MOP).")

        return {
            "nitrogen": {"value": n, "status": n_status, "optimal_range": "140 - 250 mg/kg"},
            "phosphorus": {"value": p, "status": p_status, "optimal_range": "45 - 90 mg/kg"},
            "potassium": {"value": k, "status": k_status, "optimal_range": "150 - 300 mg/kg"},
            "is_balanced": len(deficiencies) == 0,
            "deficiency_alerts": deficiencies
        }

    def generate_amendment_plan(self, ph: float, oc: float, ec: float) -> Dict[str, Any]:
        """
        Generates targeted chemical and organic soil amendments for pH correction and carbon building.
        """
        amendments = []

        # pH Correction
        if ph < 6.0:
            lime_dose = round((6.5 - ph) * 400.0, 0)
            amendments.append({
                "type": "Lime (Agricultural Calcium Carbonate)",
                "recommended_dose_kg_per_acre": lime_dose,
                "purpose": "Neutralize soil acidity and elevate pH towards 6.5"
            })
        elif ph > 7.8:
            gypsum_dose = round((ph - 7.5) * 350.0, 0)
            amendments.append({
                "type": "Agricultural Gypsum (Calcium Sulfate) / Elemental Sulfur",
                "recommended_dose_kg_per_acre": gypsum_dose,
                "purpose": "Lower alkaline soil pH and displace exchangeable sodium"
            })

        # Organic Carbon Building
        if oc < 0.75:
            compost_ton = round((0.75 - oc) * 8.0, 1)
            amendments.append({
                "type": "Well-rotted Farmyard Manure (FYM) / Vermicompost",
                "recommended_dose_tons_per_acre": compost_ton,
                "purpose": "Increase soil organic carbon content and biological active fraction"
            })

        # Salinity Control
        if ec > 2.0:
            amendments.append({
                "type": "Leaching Irrigation & Subsurface Drainage",
                "purpose": "Apply 15-20% extra leaching water to flush soluble salts below root zone"
            })

        return {
            "ph": ph,
            "organic_carbon_pct": oc,
            "electrical_conductivity_ds_m": ec,
            "amendments_required_count": len(amendments),
            "recommended_amendments": amendments
        }

    def analyze_field_soil_trend(self, field_id: int) -> Dict[str, Any]:
        """
        Analyzes multi-year soil testing trends for a field plot to verify health progression.
        """
        records = db.session.query(SoilRecord).filter_by(field_id=field_id).order_by(SoilRecord.test_date.asc()).all()
        if not records:
            return {"error": "No soil test records found for this field."}

        history = []
        for r in records:
            history.append({
                "test_date": r.test_date.strftime("%Y-%m-%d") if r.test_date else "",
                "ph": float(r.ph or 7.0),
                "nitrogen": float(r.nitrogen or 0.0),
                "phosphorus": float(r.phosphorus or 0.0),
                "potassium": float(r.potassium or 0.0),
                "organic_carbon": float(r.organic_carbon or 0.75),
                "health_score": float(r.health_score or 75.0)
            })

        initial_score = history[0]["health_score"]
        latest_score = history[-1]["health_score"]
        score_change = round(latest_score - initial_score, 1)

        trend_direction = "Improving" if score_change > 2.0 else ("Declining" if score_change < -2.0 else "Stable")

        return {
            "field_id": field_id,
            "total_test_samples": len(history),
            "initial_health_score": initial_score,
            "latest_health_score": latest_score,
            "score_change": score_change,
            "overall_trend": trend_direction,
            "historical_samples": history
        }
