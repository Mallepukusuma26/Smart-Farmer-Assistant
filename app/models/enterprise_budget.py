"""
Enterprise Budget SQLAlchemy Model for Smart Farmer Assistant.

Stores crop enterprise budgets, variable costs (seed, fertilizer, pesticide, labour, irrigation),
fixed costs (machinery depreciation, land rent), break-even yields, and projected returns.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from app.extensions import db


class EnterpriseBudget(db.Model):
    """
    SQLAlchemy model representing a crop enterprise budget statement.
    """
    __tablename__ = "enterprise_budgets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    land_area_acres = db.Column(db.Float, nullable=False, default=1.0)
    seed_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    fertilizer_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    pesticide_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    labour_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    irrigation_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    other_variable_cost_usd = db.Column(db.Float, nullable=False, default=0.0)

    machinery_depreciation_usd = db.Column(db.Float, nullable=False, default=0.0)
    land_rent_usd = db.Column(db.Float, nullable=False, default=0.0)
    other_fixed_cost_usd = db.Column(db.Float, nullable=False, default=0.0)

    expected_yield_per_acre = db.Column(db.Float, nullable=False, default=0.0)
    expected_market_price_per_unit = db.Column(db.Float, nullable=False, default=0.0)

    total_variable_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    total_fixed_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    total_production_cost_usd = db.Column(db.Float, nullable=False, default=0.0)
    gross_revenue_usd = db.Column(db.Float, nullable=False, default=0.0)
    net_profit_usd = db.Column(db.Float, nullable=False, default=0.0)

    break_even_price_per_unit = db.Column(db.Float, nullable=True, default=0.0)
    break_even_yield_per_acre = db.Column(db.Float, nullable=True, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    farmer = db.relationship("Farmer", backref=db.backref("enterprise_budgets", lazy="dynamic"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "crop_name": self.crop_name,
            "land_area_acres": self.land_area_acres,
            "seed_cost_usd": self.seed_cost_usd,
            "fertilizer_cost_usd": self.fertilizer_cost_usd,
            "pesticide_cost_usd": self.pesticide_cost_usd,
            "labour_cost_usd": self.labour_cost_usd,
            "irrigation_cost_usd": self.irrigation_cost_usd,
            "other_variable_cost_usd": self.other_variable_cost_usd,
            "machinery_depreciation_usd": self.machinery_depreciation_usd,
            "land_rent_usd": self.land_rent_usd,
            "other_fixed_cost_usd": self.other_fixed_cost_usd,
            "expected_yield_per_acre": self.expected_yield_per_acre,
            "expected_market_price_per_unit": self.expected_market_price_per_unit,
            "total_variable_cost_usd": self.total_variable_cost_usd,
            "total_fixed_cost_usd": self.total_fixed_cost_usd,
            "total_production_cost_usd": self.total_production_cost_usd,
            "gross_revenue_usd": self.gross_revenue_usd,
            "net_profit_usd": self.net_profit_usd,
            "break_even_price_per_unit": self.break_even_price_per_unit,
            "break_even_yield_per_acre": self.break_even_yield_per_acre,
            "created_at": self.created_at.isoformat()
        }
