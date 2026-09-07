from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class FarmerProfileValidator(BaseValidator):
    """Validator for farmer profile creation and updates."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['full_name'])
        full_name = self.sanitize_string('full_name', max_length=100)
        phone = self.validate_phone('phone')
        address = self.sanitize_string('address', max_length=200)
        city = self.sanitize_string('city', max_length=100)
        state_province = self.sanitize_string('state_province', max_length=100)
        region = self.sanitize_string('region', max_length=100)
        total_land_area = self.validate_range('total_land_area', min_val=0.0, max_val=10000.0)
        experience_years = self.validate_range('experience_years', min_val=0, max_val=80)
        primary_farming_type = self.validate_choice('primary_farming_type', ['Crop Farming', 'Livestock', 'Mixed', 'Horticulture'])

        if not self.is_valid():
            return {}

        return {
            'full_name': full_name,
            'phone': phone,
            'address': address,
            'city': city,
            'state_province': state_province,
            'region': region,
            'total_land_area': total_land_area or 0.0,
            'experience_years': int(experience_years or 0),
            'primary_farming_type': primary_farming_type or 'Crop Farming',
            'main_crop_type': self.sanitize_string('main_crop_type', max_length=50)
        }
