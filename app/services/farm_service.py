from typing import Dict, Any, List, Optional, Tuple
from app.repositories.farm_repository import FarmRepository
from app.repositories.field_repository import FieldRepository
from app.models.farm import Farm
from app.models.field import Field
from app.extensions import db

class FarmService:
    """Domain Service for managing farm properties, plot divisions, equipment, and GPS boundaries."""

    def __init__(self, farm_repo: Optional[FarmRepository] = None, field_repo: Optional[FieldRepository] = None):
        self.farm_repo = farm_repo or FarmRepository()
        self.field_repo = field_repo or FieldRepository()

    def get_farms_by_farmer_id(self, farmer_id: int) -> List[Farm]:
        """Retrieve all farms belonging to a farmer."""
        return self.farm_repo.get_farms_by_farmer(farmer_id)

    def get_farm_by_id(self, farm_id: int) -> Optional[Farm]:
        """Retrieve farm property by ID."""
        return self.farm_repo.get_by_id(farm_id)

    def get_fields_by_farm_id(self, farm_id: int) -> List[Field]:
        """Retrieve all fields registered under a farm."""
        return db.session.query(Field).filter_by(farm_id=farm_id).all() if hasattr(self.field_repo, 'filter_by') else self.field_repo.get_all()

    def get_field_by_id(self, field_id: int) -> Optional[Field]:
        """Retrieve field details by ID."""
        return self.field_repo.get_by_id(field_id)

    def create_farm(
        self,
        farmer_id: int,
        name: str,
        location: str,
        total_area: float,
        unit: str = 'Acres',
        ownership_type: str = 'Owned',
        default_soil_type: str = 'Loamy',
        county_district: Optional[str] = None,
        state: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Farm:
        """Create a new farm property for a farmer."""
        return self.farm_repo.create(
            farmer_id=farmer_id,
            name=name,
            location=location,
            county_district=county_district,
            state=state,
            total_area=float(total_area),
            unit=unit,
            ownership_type=ownership_type,
            default_soil_type=default_soil_type,
            notes=notes
        )

    def update_farm(self, farm_id: int, farmer_id: int, **kwargs) -> Tuple[Optional[Farm], str]:
        """Update existing farm property details."""
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm or farm.farmer_id != farmer_id:
            return None, "Farm not found or access denied."

        updated = self.farm_repo.update(farm, **kwargs)
        return updated, "Farm updated successfully."

    def delete_farm(self, farm_id: int, farmer_id: int) -> Tuple[bool, str]:
        """Delete farm and associated field plot divisions."""
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm or farm.farmer_id != farmer_id:
            return False, "Farm not found or access denied."

        self.farm_repo.delete(farm)
        return True, "Farm deleted successfully."

    def create_field(
        self,
        farm_id: int,
        field_name: str,
        area: float,
        soil_type: str = 'Loamy',
        irrigation_type: str = 'Drip',
        farming_method: str = 'Conventional',
        notes: Optional[str] = None
    ) -> Field:
        """Create a new field plot division within a farm."""
        return self.field_repo.create(
            farm_id=farm_id,
            field_name=field_name,
            area=float(area),
            soil_type=soil_type,
            irrigation_type=irrigation_type,
            farming_method=farming_method,
            notes=notes
        )

    def update_field(self, field_id: int, **kwargs) -> Optional[Field]:
        """Update field plot attributes."""
        field = self.field_repo.get_by_id(field_id)
        if not field:
            return None
        return self.field_repo.update(field, **kwargs)

    def delete_field(self, field_id: int) -> bool:
        """Delete field plot."""
        return self.field_repo.delete_by_id(field_id)

    def set_field_gps_polygon(self, field_id: int, coordinates: List[Tuple[float, float]]) -> List[Any]:
        """Set GPS polygon boundary vertices for field plot."""
        return self.field_repo.save_boundary_coordinates(field_id, coordinates)
