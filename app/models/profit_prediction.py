from datetime import datetime
from typing import Dict, Any, List, Optional
from app.extensions import db

class ProfitPrediction(db.Model):
    """Profit forecasting model output for a field/crop cycle."""
    __tablename__ = 'profit_predictions'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='RESTRICT'), nullable=False)
    expected_yield_tons = db.Column(db.Float, nullable=False)
    expected_selling_price = db.Column(db.Float, nullable=False)
    estimated_expenses = db.Column(db.Float, nullable=False)
    expected_revenue = db.Column(db.Float, nullable=False)
    expected_profit = db.Column(db.Float, nullable=False)
    profit_margin_percent = db.Column(db.Float, default=0.0)
    roi_percent = db.Column(db.Float, default=0.0)
    break_even_yield = db.Column(db.Float, default=0.0)
    break_even_price = db.Column(db.Float, default=0.0)
    risk_level = db.Column(db.String(20), default='Low') # Low, Moderate, High
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    crop = db.relationship('Crop')

    def compute_financials(self) -> None:
        """Compute expected revenue, profit, profit margin, ROI, and break-even points."""
        self.expected_revenue = round(self.expected_yield_tons * self.expected_selling_price, 2)
        self.expected_profit = round(self.expected_revenue - self.estimated_expenses, 2)
        if self.expected_revenue > 0:
            self.profit_margin_percent = round((self.expected_profit / self.expected_revenue) * 100.0, 2)
        else:
            self.profit_margin_percent = 0.0

        if self.estimated_expenses > 0:
            self.roi_percent = round((self.expected_profit / self.estimated_expenses) * 100.0, 2)
        else:
            self.roi_percent = 0.0

        if self.expected_selling_price > 0:
            self.break_even_yield = round(self.estimated_expenses / self.expected_selling_price, 2)
        else:
            self.break_even_yield = 0.0

        if self.expected_yield_tons > 0:
            self.break_even_price = round(self.estimated_expenses / self.expected_yield_tons, 2)
        else:
            self.break_even_price = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else 'Unknown',
            'expected_yield_tons': self.expected_yield_tons,
            'expected_selling_price': self.expected_selling_price,
            'estimated_expenses': self.estimated_expenses,
            'expected_revenue': self.expected_revenue,
            'expected_profit': self.expected_profit,
            'profit_margin_percent': round(self.profit_margin_percent, 2),
            'roi_percent': round(self.roi_percent, 2),
            'break_even_yield': round(self.break_even_yield, 2),
            'break_even_price': round(self.break_even_price, 2),
            'risk_level': self.risk_level,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self) -> str:
        return f"<ProfitPrediction id={self.id} expected_profit={self.expected_profit}>"


class ProfitScenario(db.Model):
    """What-if scenario simulation (Best Case, Base Case, Worst Case)."""
    __tablename__ = 'profit_scenarios'

    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('profit_predictions.id', ondelete='CASCADE'), nullable=False)
    scenario_type = db.Column(db.String(30), nullable=False) # Best Case, Base Case, Worst Case
    price_multiplier = db.Column(db.Float, default=1.0) # e.g. 1.20 for +20% price surge
    yield_multiplier = db.Column(db.Float, default=1.0) # e.g. 0.80 for -20% drought yield hit
    projected_revenue = db.Column(db.Float, nullable=False)
    projected_profit = db.Column(db.Float, nullable=False)

    prediction = db.relationship('ProfitPrediction', backref=db.backref('scenarios', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'prediction_id': self.prediction_id,
            'scenario_type': self.scenario_type,
            'price_multiplier': self.price_multiplier,
            'yield_multiplier': self.yield_multiplier,
            'projected_revenue': self.projected_revenue,
            'projected_profit': self.projected_profit
        }


class ROIAnalysis(db.Model):
    """Comparative return on investment analysis across different crop options."""
    __tablename__ = 'roi_analyses'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    crop_a_name = db.Column(db.String(100), nullable=False)
    crop_a_roi_pct = db.Column(db.Float, nullable=False)
    crop_b_name = db.Column(db.String(100), nullable=False)
    crop_b_roi_pct = db.Column(db.Float, nullable=False)
    recommended_option = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_a_name': self.crop_a_name,
            'crop_a_roi_pct': self.crop_a_roi_pct,
            'crop_b_name': self.crop_b_name,
            'crop_b_roi_pct': self.crop_b_roi_pct,
            'recommended_option': self.recommended_option,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

