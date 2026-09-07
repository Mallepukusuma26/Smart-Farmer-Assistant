from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class SoilRecordValidator(BaseValidator):
    """Validator for Soil Analysis inputs (pH, N, P, K, moisture, OC, EC)."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['field_id', 'ph', 'nitrogen', 'phosphorus', 'potassium'])
        field_id = self.validate_range('field_id', min_val=1)
        ph = self.validate_range('ph', min_val=0.0, max_val=14.0)
        nitrogen = self.validate_range('nitrogen', min_val=0.0, max_val=1000.0)
        phosphorus = self.validate_range('phosphorus', min_val=0.0, max_val=500.0)
        potassium = self.validate_range('potassium', min_val=0.0, max_val=1000.0)
        moisture = self.validate_range('moisture', min_val=0.0, max_val=100.0)
        organic_carbon = self.validate_range('organic_carbon', min_val=0.0, max_val=20.0)
        electrical_conductivity = self.validate_range('electrical_conductivity', min_val=0.0, max_val=50.0)

        if not self.is_valid():
            return {}

        return {
            'field_id': int(field_id) if field_id else None,
            'ph': ph if ph is not None else 6.5,
            'nitrogen': nitrogen if nitrogen is not None else 140.0,
            'phosphorus': phosphorus if phosphorus is not None else 50.0,
            'potassium': potassium if potassium is not None else 200.0,
            'moisture': moisture if moisture is not None else 25.0,
            'organic_carbon': organic_carbon if organic_carbon is not None else 0.75,
            'electrical_conductivity': electrical_conductivity if electrical_conductivity is not None else 0.5,
            'soil_type': self.validate_choice('soil_type', ['Loamy', 'Clay', 'Sandy', 'Silt', 'Peaty', 'Chalky']) or 'Loamy',
            'deficiency_summary': self.sanitize_string('deficiency_summary', max_length=500),
            'recommendation_notes': self.sanitize_string('recommendation_notes', max_length=1000)
        }
