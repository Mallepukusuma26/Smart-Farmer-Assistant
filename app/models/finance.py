from datetime import datetime, date
from typing import Dict, Any, List, Optional
from app.extensions import db

class Expense(db.Model):
    """Farm expense tracking entity for itemized cost analysis."""
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='SET NULL'), nullable=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='SET NULL'), nullable=True)
    category = db.Column(db.String(50), nullable=False) # Seeds, Fertilizers, Pesticides, Labour, Machinery, Irrigation, Electricity, Fuel, Transportation, Maintenance, Other
    amount = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=True, default=1.0)
    unit_cost = db.Column(db.Float, nullable=True, default=0.0)
    payment_method = db.Column(db.String(30), default='Cash') # Cash, Bank Transfer, Credit, UPI
    vendor_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    expense_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farm_id': self.farm_id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'category': self.category,
            'amount': self.amount,
            'quantity': self.quantity,
            'unit_cost': self.unit_cost,
            'payment_method': self.payment_method,
            'vendor_name': self.vendor_name,
            'description': self.description,
            'expense_date': self.expense_date.strftime('%Y-%m-%d') if self.expense_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self) -> str:
        return f"<Expense id={self.id} category='{self.category}' amount={self.amount}>"


class Revenue(db.Model):
    """Crop harvest revenue tracking entity."""
    __tablename__ = 'revenues'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='SET NULL'), nullable=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='RESTRICT'), nullable=False)
    quantity_sold = db.Column(db.Float, nullable=False) # e.g. Tons or Quintals
    unit = db.Column(db.String(20), default='Tons')
    selling_price_per_unit = db.Column(db.Float, nullable=False)
    total_revenue = db.Column(db.Float, nullable=False)
    buyer_name = db.Column(db.String(100), nullable=True)
    market_mandi_name = db.Column(db.String(100), nullable=True)
    payment_status = db.Column(db.String(30), default='Received') # Received, Pending, Partial
    sale_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    crop = db.relationship('Crop')

    def recalculate_total(self) -> float:
        """Recalculate total revenue based on unit price and quantity."""
        self.total_revenue = round(self.quantity_sold * self.selling_price_per_unit, 2)
        return self.total_revenue

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farm_id': self.farm_id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else 'Unknown',
            'quantity_sold': self.quantity_sold,
            'unit': self.unit,
            'selling_price_per_unit': self.selling_price_per_unit,
            'total_revenue': self.total_revenue,
            'buyer_name': self.buyer_name,
            'market_mandi_name': self.market_mandi_name,
            'payment_status': self.payment_status,
            'sale_date': self.sale_date.strftime('%Y-%m-%d') if self.sale_date else None,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self) -> str:
        return f"<Revenue id={self.id} crop_id={self.crop_id} total={self.total_revenue}>"


class MarketPrice(db.Model):
    """Local commodity market (Mandi) price index reference."""
    __tablename__ = 'market_prices'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    mandi_name = db.Column(db.String(100), nullable=False, default='Central Mandi')
    state_region = db.Column(db.String(100), nullable=False, default='Telangana')
    min_price_per_quintal = db.Column(db.Float, nullable=False)
    max_price_per_quintal = db.Column(db.Float, nullable=False)
    modal_price_per_quintal = db.Column(db.Float, nullable=False)
    price_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'mandi_name': self.mandi_name,
            'state_region': self.state_region,
            'min_price_per_quintal': self.min_price_per_quintal,
            'max_price_per_quintal': self.max_price_per_quintal,
            'modal_price_per_quintal': self.modal_price_per_quintal,
            'price_date': self.price_date.strftime('%Y-%m-%d')
        }


class CostPerAcre(db.Model):
    """Aggregated financial cost breakdown per acre by field and crop season."""
    __tablename__ = 'cost_per_acre_records'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    season_year = db.Column(db.String(30), nullable=False, default='Kharif 2026')
    seed_cost_per_acre = db.Column(db.Float, default=0.0)
    fertilizer_cost_per_acre = db.Column(db.Float, default=0.0)
    pesticide_cost_per_acre = db.Column(db.Float, default=0.0)
    labour_cost_per_acre = db.Column(db.Float, default=0.0)
    irrigation_cost_per_acre = db.Column(db.Float, default=0.0)
    machinery_cost_per_acre = db.Column(db.Float, default=0.0)
    total_cost_per_acre = db.Column(db.Float, nullable=False, default=0.0)

    field = db.relationship('Field', backref=db.backref('cost_records', lazy='dynamic', cascade='all, delete-orphan'))

    def compute_total(self) -> float:
        """Sum all itemized costs to calculate total cost per acre."""
        self.total_cost_per_acre = round(
            self.seed_cost_per_acre +
            self.fertilizer_cost_per_acre +
            self.pesticide_cost_per_acre +
            self.labour_cost_per_acre +
            self.irrigation_cost_per_acre +
            self.machinery_cost_per_acre, 2
        )
        return self.total_cost_per_acre

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_name': self.crop_name,
            'season_year': self.season_year,
            'seed_cost_per_acre': self.seed_cost_per_acre,
            'fertilizer_cost_per_acre': self.fertilizer_cost_per_acre,
            'pesticide_cost_per_acre': self.pesticide_cost_per_acre,
            'labour_cost_per_acre': self.labour_cost_per_acre,
            'irrigation_cost_per_acre': self.irrigation_cost_per_acre,
            'machinery_cost_per_acre': self.machinery_cost_per_acre,
            'total_cost_per_acre': self.total_cost_per_acre
        }


class BudgetPlan(db.Model):
    """Seasonal expense budget allocation planning and limit enforcement."""
    __tablename__ = 'budget_plans'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    season_name = db.Column(db.String(50), nullable=False) # Kharif, Rabi, Zaid
    year = db.Column(db.Integer, nullable=False, default=2026)
    allocated_budget = db.Column(db.Float, nullable=False, default=50000.0)
    spent_amount = db.Column(db.Float, default=0.0)
    is_exceeded = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    farmer = db.relationship('Farmer', backref=db.backref('budget_plans', lazy='dynamic', cascade='all, delete-orphan'))

    def update_spent(self, additional_amount: float) -> None:
        """Add expense amount and check budget overrun."""
        self.spent_amount += additional_amount
        if self.spent_amount > self.allocated_budget:
            self.is_exceeded = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'season_name': self.season_name,
            'year': self.year,
            'allocated_budget': self.allocated_budget,
            'spent_amount': self.spent_amount,
            'remaining_budget': max(0.0, self.allocated_budget - self.spent_amount),
            'is_exceeded': self.is_exceeded,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }
