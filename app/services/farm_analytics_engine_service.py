"""
Farm Analytics Engine Service Module for Smart Farmer Assistant.

Provides multi-farm benchmark aggregation, operational efficiency ratings, and land utilization optimization.
"""

from typing import Dict, Any, List, Optional
from app.extensions import db
from app.models.farm import Farm
from app.models.field import Field


class FarmAnalyticsEngineService:
    """Multi-farm benchmark aggregation and land utilization optimization engine."""

    def compute_farm_utilization_metrics(self, farmer_id: int) -> Dict[str, Any]:
        """Calculates total land registered vs cultivated field area, density metrics, and equipment load."""
        farms = db.session.query(Farm).filter_by(farmer_id=farmer_id).all()
        if not farms:
            return {"error": "No registered farms found for this farmer."}

        total_registered_acres = sum(float(f.total_area or 0.0) for f in farms)
        all_fields = []
        for farm in farms:
            fields = db.session.query(Field).filter_by(farm_id=farm.id).all()
            all_fields.extend(fields)

        total_cultivated_acres = sum(float(fd.area or 0.0) for fd in all_fields)
        utilization_rate_pct = round((total_cultivated_acres / total_registered_acres) * 100.0, 1) if total_registered_acres > 0 else 0.0

        organic_acres = sum(float(fd.area or 0.0) for fd in all_fields if (fd.farming_method or "").lower() == "organic")
        drip_acres = sum(float(fd.area or 0.0) for fd in all_fields if (fd.irrigation_type or "").lower() == "drip")

        return {
            "total_farms_count": len(farms),
            "total_fields_count": len(all_fields),
            "total_registered_acres": round(total_registered_acres, 2),
            "total_cultivated_acres": round(total_cultivated_acres, 2),
            "land_utilization_rate_pct": utilization_rate_pct,
            "organic_farming_acres": round(organic_acres, 2),
            "drip_irrigated_acres": round(drip_acres, 2),
            "drip_adoption_pct": round((drip_acres / max(0.1, total_cultivated_acres)) * 100.0, 1),
            "efficiency_grade": "A+" if utilization_rate_pct >= 85.0 else ("B" if utilization_rate_pct >= 60.0 else "C")
        }
