"""
Field Intelligence Service Module for Smart Farmer Assistant.

Provides detailed plot-level field analytics, historical crop performance tracking,
soil test trends, yield ranking, profitability per field, and crop sequence recommendations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.extensions import db
from app.models.field import Field
from app.models.soil import SoilRecord
from app.models.finance import Expense, Revenue
from app.repositories.field_repository import FieldRepository


class FieldIntelligenceService:
    """
    Service for field plot management, crop history compilation,
    soil fertility progression, and field profitability ranking.
    """

    def __init__(self, field_repo: Optional[FieldRepository] = None):
        self.field_repo = field_repo or FieldRepository()

    def get_field_comprehensive_profile(self, field_id: int) -> Dict[str, Any]:
        """
        Gathers complete history and telemetry for a single field plot.
        """
        field = self.field_repo.get_by_id(field_id)
        if not field:
            return {"error": f"Field plot with ID {field_id} not found."}

        soil_records = db.session.query(SoilRecord).filter_by(field_id=field_id).order_by(SoilRecord.test_date.desc()).all()
        latest_soil = soil_records[0].to_dict() if soil_records else None

        expenses = db.session.query(Expense).filter_by(field_id=field_id).all()
        revenues = db.session.query(Revenue).filter_by(field_id=field_id).all()

        total_cost = sum(float(e.amount or 0.0) for e in expenses)
        total_rev = sum(float(r.total_amount or (r.quantity_sold * r.selling_price_per_unit) or 0.0) for r in revenues)
        net_profit = total_rev - total_cost

        area = float(field.area or 1.0)
        cost_per_acre = round(total_cost / area, 2)
        rev_per_acre = round(total_rev / area, 2)
        profit_per_acre = round(net_profit / area, 2)

        health_index = latest_soil.get("health_score", 75.0) if latest_soil else 70.0

        return {
            "field_id": field.id,
            "field_name": field.field_name,
            "farm_id": field.farm_id,
            "area_acres": area,
            "soil_type": field.soil_type or "Loamy",
            "irrigation_type": field.irrigation_type or "Drip",
            "farming_method": field.farming_method or "Conventional",
            "total_soil_tests_conducted": len(soil_records),
            "latest_soil_health_score": health_index,
            "total_expenses": round(total_cost, 2),
            "total_revenue": round(total_rev, 2),
            "net_profit": round(net_profit, 2),
            "cost_per_acre": cost_per_acre,
            "revenue_per_acre": rev_per_acre,
            "profit_per_acre": profit_per_acre,
            "is_profitable": net_profit >= 0,
            "notes": field.notes
        }

    def rank_fields_by_profitability(self, farm_id: int) -> List[Dict[str, Any]]:
        """
        Ranks all field plots within a farm by net profit per acre.
        """
        fields = db.session.query(Field).filter_by(farm_id=farm_id).all()
        profiles = [self.get_field_comprehensive_profile(f.id) for f in fields]
        return sorted(profiles, key=lambda x: x.get("profit_per_acre", 0.0), reverse=True)

    def rank_fields_by_soil_health(self, farm_id: int) -> List[Dict[str, Any]]:
        """
        Ranks all fields within a farm by their latest soil health score index.
        """
        fields = db.session.query(Field).filter_by(farm_id=farm_id).all()
        profiles = [self.get_field_comprehensive_profile(f.id) for f in fields]
        return sorted(profiles, key=lambda x: x.get("latest_soil_health_score", 0.0), reverse=True)

    def calculate_field_water_budget(self, field_id: int, crop_type: str = "Wheat") -> Dict[str, Any]:
        """
        Calculates seasonal water consumption and budget for a specific field plot.
        """
        field = self.field_repo.get_by_id(field_id)
        if not field:
            return {"error": "Field not found"}

        area = float(field.area or 1.0)
        water_req_mm = 450.0  # Base water requirement in mm

        if crop_type.lower() in ["rice", "paddy", "sugarcane"]:
            water_req_mm = 1200.0
        elif crop_type.lower() in ["maize", "cotton", "soybean"]:
            water_req_mm = 600.0
        elif crop_type.lower() in ["mustard", "chickpea", "pulses"]:
            water_req_mm = 300.0

        # Convert mm to m3 per acre (1 mm over 1 acre = 4.04686 m3)
        water_m3 = round(water_req_mm * 4.04686 * area, 1)

        irrigation_eff = 0.90 if (field.irrigation_type or "").lower() == "drip" else (
            0.75 if (field.irrigation_type or "").lower() == "sprinkler" else 0.60
        )

        effective_water_needed_m3 = round(water_m3 / irrigation_eff, 1)

        return {
            "field_id": field.id,
            "field_name": field.field_name,
            "area_acres": area,
            "crop_type": crop_type,
            "base_water_requirement_mm": water_req_mm,
            "net_water_required_m3": water_m3,
            "irrigation_system": field.irrigation_type or "Drip",
            "irrigation_efficiency_pct": round(irrigation_eff * 100.0, 1),
            "gross_water_needed_m3": effective_water_needed_m3,
            "recommended_irrigation_rounds": math.ceil(water_req_mm / 40.0)
        }
