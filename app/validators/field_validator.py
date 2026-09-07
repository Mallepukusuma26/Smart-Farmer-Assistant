from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class FieldValidator(BaseValidator):
    """Validator for Field plot creation and updating."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['farm_id', 'field_name', 'area', 'soil_type'])
        farm_id = self.validate_range('farm_id', min_val=1)
        field_name = self.sanitize_string('field_name', max_length=100)
        area = self.validate_range('area', min_val=0.01, max_val=10000.0)
        soil_type = self.validate_choice('soil_type', ['Loamy', 'Clay', 'Sandy', 'Silt', 'Peaty', 'Chalky'])
        irrigation_type = self.validate_choice('irrigation_type', ['Drip', 'Sprinkler', 'Flood', 'Rainfed'])
        farming_method = self.validate_choice('farming_method', ['Conventional', 'Organic', 'Hydroponic'])

        if not self.is_valid():
            return {}

        return {
            'farm_id': int(farm_id) if farm_id else None,
            'field_name': field_name,
            'area': area or 1.0,
            'soil_type': soil_type or 'Loamy',
            'irrigation_type': irrigation_type or 'Drip',
            'farming_method': farming_method or 'Conventional',
            'current_status': self.validate_choice('current_status', ['Active', 'Fallow', 'Harvested', 'Preparing']) or 'Active',
            'drainage_quality': self.validate_choice('drainage_quality', ['Excellent', 'Good', 'Fair', 'Poor']) or 'Good',
            'sunlight_exposure': self.validate_choice('sunlight_exposure', ['Full Sun', 'Partial Shade', 'Shade']) or 'Full Sun',
            'notes': self.sanitize_string('notes', max_length=1000)
        }
