from datetime import datetime
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
    break_even_yield = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    crop = db.relationship('Crop')

    def to_dict(self):
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
            'break_even_yield': round(self.break_even_yield, 2),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self):
        return f"<ProfitPrediction id={self.id} expected_profit={self.expected_profit}>"
