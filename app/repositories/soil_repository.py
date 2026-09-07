from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.soil import SoilRecord, SoilSample, SoilImprovementPlan, SoilNutrientTrend, SoilTestLab
from app.repositories.base_repository import BaseRepository

class SoilRepository(BaseRepository[SoilRecord]):
    """Data Access Repository for Soil Analysis, Samples, Health Scores, and Amendment Plans."""

    def __init__(self):
        super().__init__(SoilRecord)

    def get_latest_by_field(self, field_id: int) -> Optional[SoilRecord]:
        """Fetch most recent soil analysis test for a field."""
        return db.session.query(SoilRecord).filter_by(field_id=field_id).order_by(SoilRecord.test_date.desc()).first()

    def get_records_by_field(self, field_id: int) -> List[SoilRecord]:
        """Fetch full soil test history for a field."""
        return db.session.query(SoilRecord).filter_by(field_id=field_id).order_by(SoilRecord.test_date.desc()).all()

    def get_avg_soil_health_score(self, farmer_id: Optional[int] = None) -> float:
        """Calculate average soil health score across fields."""
        query = db.session.query(func.avg(SoilRecord.health_score))
        if farmer_id:
            from app.models.field import Field
            from app.models.farm import Farm
            query = query.join(Field, SoilRecord.field_id == Field.id).join(Farm, Field.farm_id == Farm.id).filter(Farm.farmer_id == farmer_id)
        val = query.scalar()
        return round(float(val), 1) if val else 75.0

    def search_soil_records(
        self,
        field_id: Optional[int] = None,
        soil_type: Optional[str] = None,
        min_health: Optional[float] = None,
        max_health: Optional[float] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[SoilRecord], int, int]:
        """Search soil records with filtering by health score range and soil texture class."""
        query = db.session.query(SoilRecord)

        if field_id:
            query = query.filter_by(field_id=field_id)

        if soil_type:
            query = query.filter(SoilRecord.soil_type == soil_type)

        if min_health is not None:
            query = query.filter(SoilRecord.health_score >= min_health)

        if max_health is not None:
            query = query.filter(SoilRecord.health_score <= max_health)

        return self.paginate(page=page, per_page=per_page, query=query.order_by(SoilRecord.test_date.desc()))

    def add_soil_sample(self, field_id: int, sample_code: str, sampling_depth_cm: float = 15.0, sample_lat: Optional[float] = None, sample_lng: Optional[float] = None, lab_name: str = 'Local Agronomy Lab', notes: Optional[str] = None) -> SoilSample:
        """Register raw field soil sample collected for testing."""
        sample = SoilSample(
            field_id=field_id,
            sample_code=sample_code,
            sampling_depth_cm=sampling_depth_cm,
            sample_latitude=sample_lat,
            sample_longitude=sample_lng,
            lab_name=lab_name,
            notes=notes
        )
        db.session.add(sample)
        db.session.commit()
        return sample

    def add_improvement_plan(self, soil_record_id: int, amendment_type: str, target_parameter: str, dose_kg_per_acre: float, estimated_cost: float = 0.0, timeframe_days: int = 30) -> SoilImprovementPlan:
        """Add recommended soil amendment plan based on deficiency detection."""
        plan = SoilImprovementPlan(
            soil_record_id=soil_record_id,
            amendment_type=amendment_type,
            target_parameter=target_parameter,
            recommended_dose_kg_per_acre=dose_kg_per_acre,
            estimated_cost=estimated_cost,
            timeframe_days=timeframe_days
        )
        db.session.add(plan)
        db.session.commit()
        return plan

    def get_improvement_plans(self, soil_record_id: int) -> List[SoilImprovementPlan]:
        """Fetch amendment plans attached to a soil test record."""
        return db.session.query(SoilImprovementPlan).filter_by(soil_record_id=soil_record_id).all()
