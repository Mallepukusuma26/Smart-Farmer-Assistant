from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class FarmValidator(BaseValidator):
    """Validator for Farm registration and modifications."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['name', 'location', 'total_area'])
        name = self.sanitize_string('name', max_length=100)
        location = self.sanitize_string('location', max_length=150)
        total_area = self.validate_range('total_area', min_val=0.1, max_val=50000.0)
        unit = self.validate_choice('unit', ['Acres', 'Hectares', 'SqMeters'])
        ownership = self.validate_choice('ownership_type', ['Owned', 'Leased', 'Rented', 'Shared'])
        soil_type = self.validate_choice('default_soil_type', ['Loamy', 'Clay', 'Sandy', 'Silt', 'Peaty', 'Chalky'])

        if not self.is_valid():
            return {}

        return {
            'name': name,
            'location': location,
            'county_district': self.sanitize_string('county_district', max_length=100),
            'state': self.sanitize_string('state', max_length=100),
            'total_area': total_area or 1.0,
            'unit': unit or 'Acres',
            'ownership_type': ownership or 'Owned',
            'default_soil_type': soil_type or 'Loamy',
            'water_source_primary': self.sanitize_string('water_source_primary', max_length=50) or 'Well Water',
            'elevation_meters': self.validate_range('elevation_meters', min_val=-100.0, max_val=9000.0) or 100.0,
            'slope_percentage': self.validate_range('slope_percentage', min_val=0.0, max_val=90.0) or 2.0,
            'notes': self.sanitize_string('notes', max_length=1000)
        }
