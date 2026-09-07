from typing import Optional, List, Dict, Any, Tuple
from app.repositories.farmer_repository import FarmerRepository
from app.models.farmer import Farmer, FarmerPreference

class FarmerService:
    """Domain Service for managing farmer profiles, Preferences, Documents, and Activity Streams."""

    def __init__(self, repository: Optional[FarmerRepository] = None):
        self.repository = repository or FarmerRepository()

    def get_farmer_by_user_id(self, user_id: int) -> Optional[Farmer]:
        """Fetch farmer profile linked to user ID."""
        return self.repository.find_by_user_id(user_id)

    def create_or_update_profile(self, user_id: int, full_name: str, phone: Optional[str] = None, address: Optional[str] = None, region: Optional[str] = None, total_land_area: float = 0.0, primary_farming_type: str = 'Crop Farming', main_crop_type: Optional[str] = None, experience_years: int = 0) -> Farmer:
        """Create or update farmer profile details."""
        farmer = self.repository.find_by_user_id(user_id)
        if not farmer:
            farmer = self.repository.create(
                user_id=user_id,
                full_name=full_name,
                phone=phone,
                address=address,
                region=region,
                total_land_area=total_land_area,
                primary_farming_type=primary_farming_type,
                main_crop_type=main_crop_type,
                experience_years=experience_years
            )
            self.repository.log_activity(farmer.id, 'PROFILE_CREATE', 'Farmer profile created.')
        else:
            self.repository.update(
                farmer,
                full_name=full_name,
                phone=phone,
                address=address,
                region=region,
                total_land_area=total_land_area,
                primary_farming_type=primary_farming_type,
                main_crop_type=main_crop_type,
                experience_years=experience_years
            )
            self.repository.log_activity(farmer.id, 'PROFILE_UPDATE', 'Farmer profile updated.')
        return farmer

    def get_full_farmer_dashboard_data(self, farmer_id: int) -> Dict[str, Any]:
        """Fetch complete aggregate farmer overview dashboard metrics."""
        farmer = self.repository.get_by_id(farmer_id)
        if not farmer:
            return {}

        farms = [f.to_dict() for f in farmer.farms.all()]
        activities = self.repository.get_recent_activities(farmer_id, limit=10)
        docs = self.repository.get_farmer_documents(farmer_id)

        return {
            'farmer_profile': farmer.to_dict(),
            'total_farms': len(farms),
            'total_land_acres': farmer.total_land_area,
            'farms': farms,
            'recent_activities': [a.to_dict() for a in activities],
            'documents': [d.to_dict() for d in docs]
        }
