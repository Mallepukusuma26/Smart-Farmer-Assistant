from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, and_, func
from app.extensions import db
from app.models.farm import Farm, FarmDocument, FarmLocation, FarmEquipment, FarmCertifications, FarmResource
from app.repositories.base_repository import BaseRepository

class FarmRepository(BaseRepository[Farm]):
    """Data Access Repository for Farm properties, locations, equipment, and certifications."""

    def __init__(self):
        super().__init__(Farm)

    def get_farms_by_farmer(self, farmer_id: int) -> List[Farm]:
        """Get all farms owned or managed by a farmer."""
        return db.session.query(Farm).filter_by(farmer_id=farmer_id).order_by(Farm.name.asc()).all()

    def count_farms_by_farmer(self, farmer_id: int) -> int:
        """Count total farms owned by farmer."""
        return db.session.query(func.count(Farm.id)).filter_by(farmer_id=farmer_id).scalar() or 0

    def calculate_total_land_area(self, farmer_id: int) -> float:
        """Sum total land area in acres across all farms of a farmer."""
        total = db.session.query(func.sum(Farm.total_area)).filter_by(farmer_id=farmer_id).scalar()
        return round(float(total), 2) if total else 0.0

    def search_farms(
        self,
        farmer_id: Optional[int] = None,
        keyword: Optional[str] = None,
        ownership_type: Optional[str] = None,
        soil_type: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[Farm], int, int]:
        """Search farms with filtering across location, name, and soil type."""
        query = db.session.query(Farm)

        if farmer_id:
            query = query.filter_by(farmer_id=farmer_id)

        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(
                or_(
                    Farm.name.ilike(term),
                    Farm.location.ilike(term),
                    Farm.county_district.ilike(term),
                    Farm.state.ilike(term)
                )
            )

        if ownership_type:
            query = query.filter(Farm.ownership_type == ownership_type)

        if soil_type:
            query = query.filter(Farm.default_soil_type == soil_type)

        return self.paginate(page=page, per_page=per_page, query=query.order_by(Farm.created_at.desc()))

    def set_farm_location(self, farm_id: int, latitude: float, longitude: float, agro_climatic_zone: str = 'Zone 4 - Temperate', micro_climate_notes: Optional[str] = None) -> FarmLocation:
        """Set or update GPS coordinates and agro-climatic zone for farm."""
        loc = db.session.query(FarmLocation).filter_by(farm_id=farm_id).first()
        if not loc:
            loc = FarmLocation(
                farm_id=farm_id,
                latitude=latitude,
                longitude=longitude,
                agro_climatic_zone=agro_climatic_zone,
                micro_climate_notes=micro_climate_notes
            )
            db.session.add(loc)
        else:
            loc.latitude = latitude
            loc.longitude = longitude
            loc.agro_climatic_zone = agro_climatic_zone
            if micro_climate_notes:
                loc.micro_climate_notes = micro_climate_notes
        db.session.commit()
        return loc

    def add_equipment(self, farm_id: int, name: str, equipment_type: str = 'Tractor', purchase_year: int = 2022, condition_status: str = 'Operational') -> FarmEquipment:
        """Register equipment/machinery for farm."""
        equip = FarmEquipment(
            farm_id=farm_id,
            name=name,
            equipment_type=equipment_type,
            purchase_year=purchase_year,
            condition_status=condition_status
        )
        db.session.add(equip)
        db.session.commit()
        return equip

    def get_equipment_by_farm(self, farm_id: int) -> List[FarmEquipment]:
        """Fetch machinery inventory of a farm."""
        return db.session.query(FarmEquipment).filter_by(farm_id=farm_id).all()

    def add_certification(self, farm_id: int, certification_name: str, issuing_body: str, valid_until) -> FarmCertifications:
        """Record organic/GAP certification earned by farm."""
        cert = FarmCertifications(
            farm_id=farm_id,
            certification_name=certification_name,
            issuing_body=issuing_body,
            valid_until=valid_until
        )
        db.session.add(cert)
        db.session.commit()
        return cert

    def add_resource(self, farm_id: int, resource_name: str, quantity_available: float = 0.0, unit_of_measure: str = 'Kg') -> FarmResource:
        """Add inventory resource to farm."""
        res = FarmResource(
            farm_id=farm_id,
            resource_name=resource_name,
            quantity_available=quantity_available,
            unit_of_measure=unit_of_measure
        )
        db.session.add(res)
        db.session.commit()
        return res
