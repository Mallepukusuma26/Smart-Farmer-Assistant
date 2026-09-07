from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class CropValidator(BaseValidator):
    """Validator for Crop Catalog species parameters."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['name', 'category', 'season'])
        name = self.sanitize_string('name', max_length=100)
        category = self.validate_choice('category', ['Cereal', 'Pulse', 'Oilseed', 'Vegetable', 'Fruit', 'Cash Crop'])
        season = self.validate_choice('season', ['Kharif', 'Rabi', 'Zaid', 'Perennial', 'All Season'])
        min_ph = self.validate_range('min_ph', min_val=3.0, max_val=11.0)
        max_ph = self.validate_range('max_ph', min_val=3.0, max_val=11.0)
        duration_days = self.validate_range('duration_days', min_val=10, max_val=1000)

        if min_ph and max_ph and min_ph > max_ph:
            self.add_error('min_ph', 'Minimum pH cannot be greater than Maximum pH.')

        if not self.is_valid():
            return {}

        return {
            'name': name,
            'scientific_name': self.sanitize_string('scientific_name', max_length=150),
            'category': category or 'Cereal',
            'season': season or 'Kharif',
            'min_ph': min_ph or 5.5,
            'max_ph': max_ph or 7.5,
            'min_temp': self.validate_range('min_temp', min_val=-10.0, max_val=60.0) or 15.0,
            'max_temp': self.validate_range('max_temp', min_val=-10.0, max_val=60.0) or 35.0,
            'min_rainfall': self.validate_range('min_rainfall', min_val=0.0, max_val=10000.0) or 400.0,
            'max_rainfall': self.validate_range('max_rainfall', min_val=0.0, max_val=10000.0) or 1500.0,
            'min_n': self.validate_range('min_n', min_val=0.0) or 60.0,
            'min_p': self.validate_range('min_p', min_val=0.0) or 30.0,
            'min_k': self.validate_range('min_k', min_val=0.0) or 40.0,
            'duration_days': int(duration_days or 120),
            'base_yield_per_acre': self.validate_range('base_yield_per_acre', min_val=0.1) or 2.5,
            'water_req_mm': self.validate_range('water_req_mm', min_val=10.0) or 500.0,
            'ideal_soil_type': self.validate_choice('ideal_soil_type', ['Loamy', 'Clay', 'Sandy', 'Silt', 'Peaty', 'Chalky']) or 'Loamy',
            'description': self.sanitize_string('description', max_length=2000)
        }
