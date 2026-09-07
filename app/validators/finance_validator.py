from typing import Dict, Any, Optional
from datetime import datetime, date
from app.validators.base_validator import BaseValidator

class ExpenseValidator(BaseValidator):
    """Validator for farm expense records."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['farmer_id', 'category', 'amount'])
        farmer_id = self.validate_range('farmer_id', min_val=1)
        category = self.validate_choice('category', ['Seeds', 'Fertilizers', 'Pesticides', 'Labour', 'Machinery', 'Irrigation', 'Electricity', 'Fuel', 'Transportation', 'Maintenance', 'Other'])
        amount = self.validate_range('amount', min_val=0.01, max_val=10000000.0)

        date_str = self.data.get('expense_date')
        parsed_date = date.today()
        if date_str:
            try:
                parsed_date = datetime.strptime(str(date_str).strip(), '%Y-%m-%d').date()
            except ValueError:
                self.add_error('expense_date', 'Expense date must be YYYY-MM-DD.')

        if not self.is_valid():
            return {}

        return {
            'farmer_id': int(farmer_id) if farmer_id else None,
            'farm_id': self.data.get('farm_id'),
            'field_id': self.data.get('field_id'),
            'crop_id': self.data.get('crop_id'),
            'category': category or 'Other',
            'amount': amount or 0.0,
            'quantity': self.validate_range('quantity', min_val=0.01) or 1.0,
            'unit_cost': self.validate_range('unit_cost', min_val=0.0) or 0.0,
            'payment_method': self.validate_choice('payment_method', ['Cash', 'Bank Transfer', 'Credit', 'UPI']) or 'Cash',
            'vendor_name': self.sanitize_string('vendor_name', max_length=100),
            'description': self.sanitize_string('description', max_length=255),
            'expense_date': parsed_date
        }


class RevenueValidator(BaseValidator):
    """Validator for harvest revenue records."""

    def validate(self) -> Dict[str, Any]:
        self.validate_required(['farmer_id', 'crop_id', 'quantity_sold', 'selling_price_per_unit'])
        farmer_id = self.validate_range('farmer_id', min_val=1)
        crop_id = self.validate_range('crop_id', min_val=1)
        quantity = self.validate_range('quantity_sold', min_val=0.01)
        price = self.validate_range('selling_price_per_unit', min_val=0.01)

        date_str = self.data.get('sale_date')
        parsed_date = date.today()
        if date_str:
            try:
                parsed_date = datetime.strptime(str(date_str).strip(), '%Y-%m-%d').date()
            except ValueError:
                self.add_error('sale_date', 'Sale date must be YYYY-MM-DD.')

        if not self.is_valid():
            return {}

        return {
            'farmer_id': int(farmer_id) if farmer_id else None,
            'farm_id': self.data.get('farm_id'),
            'field_id': self.data.get('field_id'),
            'crop_id': int(crop_id) if crop_id else None,
            'quantity_sold': quantity or 0.0,
            'unit': self.sanitize_string('unit', max_length=20) or 'Tons',
            'selling_price_per_unit': price or 0.0,
            'buyer_name': self.sanitize_string('buyer_name', max_length=100),
            'market_mandi_name': self.sanitize_string('market_mandi_name', max_length=100),
            'payment_status': self.validate_choice('payment_status', ['Received', 'Pending', 'Partial']) or 'Received',
            'sale_date': parsed_date,
            'notes': self.sanitize_string('notes', max_length=500)
        }
