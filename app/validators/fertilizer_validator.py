from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator

class FertilizerValidator(BaseValidator):
    """Validator for Fertilizer products and NPK percentage ratios."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['name', 'category'])
        name = self.sanitize_string('name', max_length=100)
        category = self.validate_choice('category', ['Nitrogenous', 'Phosphatic', 'Potassic', 'Complex', 'Organic'])
        n_percent = self.validate_range('n_percent', min_val=0.0, max_val=100.0)
        p_percent = self.validate_range('p_percent', min_val=0.0, max_val=100.0)
        k_percent = self.validate_range('k_percent', min_val=0.0, max_val=100.0)
        price_per_kg = self.validate_range('price_per_kg', min_val=0.0, max_val=10000.0)

        if not self.is_valid():
            return {}

        return {
            'name': name,
            'category': category or 'Complex',
            'n_percent': n_percent or 0.0,
            'p_percent': p_percent or 0.0,
            'k_percent': k_percent or 0.0,
            'sulfur_percent': self.validate_range('sulfur_percent', min_val=0.0, max_val=100.0) or 0.0,
            'zinc_percent': self.validate_range('zinc_percent', min_val=0.0, max_val=100.0) or 0.0,
            'suitable_crops': self.sanitize_string('suitable_crops', max_length=255) or 'All Crops',
            'application_notes': self.sanitize_string('application_notes', max_length=1000),
            'price_per_kg': price_per_kg or 25.0
        }
