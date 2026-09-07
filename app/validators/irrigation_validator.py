from typing import Dict, Any, Optional
from datetime import datetime, date
from app.validators.base_validator import BaseValidator

class IrrigationScheduleValidator(BaseValidator):
    """Validator for Irrigation scheduling requests."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['field_id', 'next_irrigation_date', 'water_required_liters'])
        field_id = self.validate_range('field_id', min_val=1)
        water_req = self.validate_range('water_required_liters', min_val=1.0, max_val=1000000.0)
        freq_days = self.validate_range('frequency_days', min_val=1, max_val=90)
        duration_mins = self.validate_range('duration_minutes', min_val=5, max_val=1440)
        method = self.validate_choice('method', ['Drip', 'Sprinkler', 'Surface', 'Sub-irrigation'])

        date_str = self.data.get('next_irrigation_date')
        parsed_date = None
        if date_str:
            try:
                parsed_date = datetime.strptime(str(date_str).strip(), '%Y-%m-%d').date()
            except ValueError:
                self.add_error('next_irrigation_date', 'Date must be formatted as YYYY-MM-DD.')

        if not self.is_valid():
            return {}

        return {
            'field_id': int(field_id) if field_id else None,
            'crop_cycle_id': self.data.get('crop_cycle_id'),
            'water_source_id': self.data.get('water_source_id'),
            'water_required_liters': water_req or 1000.0,
            'next_irrigation_date': parsed_date or date.today(),
            'frequency_days': int(freq_days or 5),
            'duration_minutes': int(duration_mins or 60),
            'method': method or 'Drip',
            'status': self.validate_choice('status', ['Scheduled', 'Completed', 'Skipped', 'Overdue']) or 'Scheduled',
            'priority_level': self.validate_choice('priority_level', ['Low', 'Medium', 'High', 'Critical']) or 'Medium',
            'notes': self.sanitize_string('notes', max_length=500)
        }
