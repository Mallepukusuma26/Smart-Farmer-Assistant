from datetime import datetime
from app.extensions import db

class Expense(db.Model):
    """Farm expense tracking entity."""
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='SET NULL'), nullable=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='SET NULL'), nullable=True)
    category = db.Column(db.String(50), nullable=False) # Seeds, Fertilizers, Pesticides, Labour, Machinery, Irrigation, Electricity, Fuel, Transportation, Maintenance, Other
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    expense_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farm_id': self.farm_id,
            'field_id': self.field_id,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'expense_date': self.expense_date.strftime('%Y-%m-%d') if self.expense_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
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
    sale_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    crop = db.relationship('Crop')

    def to_dict(self):
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
            'sale_date': self.sale_date.strftime('%Y-%m-%d') if self.sale_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f"<Revenue id={self.id} total={self.total_revenue}>"
