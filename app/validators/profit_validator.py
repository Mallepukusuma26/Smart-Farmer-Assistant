from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class ProfitPredictionValidator(BaseValidator):
    """Validator for farm profitability forecast requests."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['farmer_id', 'field_id', 'crop_id', 'expected_yield_tons', 'expected_selling_price', 'estimated_expenses'])
        farmer_id = self.validate_range('farmer_id', min_val=1)
        field_id = self.validate_range('field_id', min_val=1)
        crop_id = self.validate_range('crop_id', min_val=1)
        expected_yield = self.validate_range('expected_yield_tons', min_val=0.01)
        selling_price = self.validate_range('expected_selling_price', min_val=0.01)
        expenses = self.validate_range('estimated_expenses', min_val=0.0)

        if not self.is_valid():
            return {}

        return {
            'farmer_id': int(farmer_id) if farmer_id else None,
            'field_id': int(field_id) if field_id else None,
            'crop_id': int(crop_id) if crop_id else None,
            'expected_yield_tons': expected_yield or 0.0,
            'expected_selling_price': selling_price or 0.0,
            'estimated_expenses': expenses or 0.0,
            'risk_level': self.validate_choice('risk_level', ['Low', 'Moderate', 'High']) or 'Low'
        }
