from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.field import Field, FieldBoundary, FieldCropHistory, FieldSoilTrend, FieldIrrigationLog
from app.repositories.base_repository import BaseRepository

class FieldRepository(BaseRepository[Field]):
    """Data Access Repository for Field plots, boundary coordinates, crop history, and soil trends."""

    def __init__(self):
        super().__init__(Field)

    def get_fields_by_farm(self, farm_id: int) -> List[Field]:
        """Fetch all field plot divisions in a specific farm."""
        return db.session.query(Field).filter_by(farm_id=farm_id).order_by(Field.field_name.asc()).all()

    def get_fields_by_farmer(self, farmer_id: int) -> List[Field]:
        """Fetch all fields owned by a farmer across all their farms."""
        from app.models.farm import Farm
        return db.session.query(Field).join(Farm, Field.farm_id == Farm.id).filter(Farm.farmer_id == farmer_id).all()

    def count_active_fields(self, farm_id: Optional[int] = None) -> int:
        """Count active field plots."""
        query = db.session.query(func.count(Field.id)).filter(Field.current_status == 'Active')
        if farm_id:
            query = query.filter(Field.farm_id == farm_id)
        return query.scalar() or 0

    def search_fields(
        self,
        farm_id: Optional[int] = None,
        soil_type: Optional[str] = None,
        irrigation_type: Optional[str] = None,
        current_status: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[Field], int, int]:
        """Search fields with filtering parameters."""
        query = db.session.query(Field)

        if farm_id:
            query = query.filter_by(farm_id=farm_id)

        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(Field.field_name.ilike(term))

        if soil_type:
            query = query.filter(Field.soil_type == soil_type)

        if irrigation_type:
            query = query.filter(Field.irrigation_type == irrigation_type)

        if current_status:
            query = query.filter(Field.current_status == current_status)

        return self.paginate(page=page, per_page=per_page, query=query.order_by(Field.field_name.asc()))

    def save_boundary_coordinates(self, field_id: int, coordinates: List[Tuple[float, float]]) -> List[FieldBoundary]:
        """Save list of (latitude, longitude) GPS boundary vertices for field plot mapping."""
        db.session.query(FieldBoundary).filter_by(field_id=field_id).delete()
        
        boundaries = []
        for idx, (lat, lng) in enumerate(coordinates, start=1):
            b = FieldBoundary(
                field_id=field_id,
                sequence_order=idx,
                latitude=lat,
                longitude=lng
            )
            boundaries.append(b)
            db.session.add(b)
        db.session.commit()
        return boundaries

    def get_field_boundaries(self, field_id: int) -> List[FieldBoundary]:
        """Get ordered polygon vertices for field polygon mapping."""
        return db.session.query(FieldBoundary).filter_by(field_id=field_id).order_by(FieldBoundary.sequence_order.asc()).all()

    def record_past_crop(self, field_id: int, crop_name: str, year: int = 2025, season: str = 'Kharif', yield_obtained_tons: float = 0.0) -> FieldCropHistory:
        """Record historical crop performance in field plot."""
        history = FieldCropHistory(
            field_id=field_id,
            crop_name=crop_name,
            year=year,
            season=season,
            yield_obtained_tons=yield_obtained_tons
        )
        db.session.add(history)
        db.session.commit()
        return history

    def get_crop_history(self, field_id: int) -> List[FieldCropHistory]:
        """Fetch past crop history entries for field."""
        return db.session.query(FieldCropHistory).filter_by(field_id=field_id).order_by(FieldCropHistory.year.desc()).all()

    def record_soil_trend(self, field_id: int, ph_level: float, nitrogen_level: float, phosphorus_level: float, potassium_level: float, record_date=None) -> FieldSoilTrend:
        """Record soil nutrient snapshot for temporal trend analysis."""
        from datetime import date
        if record_date is None:
            record_date = date.today()
        trend = FieldSoilTrend(
            field_id=field_id,
            ph_level=ph_level,
            nitrogen_level=nitrogen_level,
            phosphorus_level=phosphorus_level,
            potassium_level=potassium_level,
            record_date=record_date
        )
        db.session.add(trend)
        db.session.commit()
        return trend
