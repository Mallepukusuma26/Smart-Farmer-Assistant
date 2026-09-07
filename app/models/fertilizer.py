from datetime import datetime
from app.extensions import db

class Fertilizer(db.Model):
    """Fertilizer catalog entity with N-P-K nutrient composition."""
    __tablename__ = 'fertilizers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), default='Chemical', index=True) # Nitrogenous, Phosphatic, Potassic, Complex, Organic
    n_percent = db.Column(db.Float, default=0.0)
    p_percent = db.Column(db.Float, default=0.0)
    k_percent = db.Column(db.Float, default=0.0)
    sulfur_percent = db.Column(db.Float, default=0.0)
    zinc_percent = db.Column(db.Float, default=0.0)
    organic_matter_percent = db.Column(db.Float, default=0.0)
    suitable_crops = db.Column(db.String(255), default='All Crops')
    application_notes = db.Column(db.Text, nullable=True)
    price_per_kg = db.Column(db.Float, default=25.0)

    # Relationships
    inventories = db.relationship('FertilizerInventory', backref='fertilizer', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'n_percent': self.n_percent,
            'p_percent': self.p_percent,
            'k_percent': self.k_percent,
            'sulfur_percent': self.sulfur_percent,
            'zinc_percent': self.zinc_percent,
            'npk_ratio': f"{self.n_percent}-{self.p_percent}-{self.k_percent}",
            'suitable_crops': self.suitable_crops,
            'application_notes': self.application_notes,
            'price_per_kg': self.price_per_kg
        }

    def __repr__(self):
        return f"<Fertilizer id={self.id} name='{self.name}'>"


class FertilizerInventory(db.Model):
    """Farmer local stock inventory of fertilizer supplies."""
    __tablename__ = 'fertilizer_inventories'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    fertilizer_id = db.Column(db.Integer, db.ForeignKey('fertilizers.id', ondelete='RESTRICT'), nullable=False)
    stock_quantity_kg = db.Column(db.Float, nullable=False, default=0.0)
    purchase_price_per_kg = db.Column(db.Float, nullable=False, default=25.0)
    purchase_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    storage_location = db.Column(db.String(100), default='Farm Store Barn')

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'fertilizer_id': self.fertilizer_id,
            'fertilizer_name': self.fertilizer.name if self.fertilizer else 'Unknown',
            'stock_quantity_kg': self.stock_quantity_kg,
            'purchase_price_per_kg': self.purchase_price_per_kg,
            'purchase_date': self.purchase_date.strftime('%Y-%m-%d'),
            'storage_location': self.storage_location
        }


class FertilizerRecommendation(db.Model):
    """Calculated fertilizer recommendation for a specific field/crop."""
    __tablename__ = 'fertilizer_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False, index=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id', ondelete='SET NULL'), nullable=True)
    soil_record_id = db.Column(db.Integer, db.ForeignKey('soil_records.id', ondelete='SET NULL'), nullable=True)
    recommended_fertilizer = db.Column(db.String(100), nullable=False)
    quantity_kg_per_acre = db.Column(db.Float, nullable=False)
    total_quantity_kg = db.Column(db.Float, nullable=False)
    application_stage = db.Column(db.String(100), default='Basal / Sowing') # Basal, Vegetative, Flowering, Grain filling
    cost_estimate = db.Column(db.Float, default=0.0)
    safety_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'crop_id': self.crop_id,
            'recommended_fertilizer': self.recommended_fertilizer,
            'quantity_kg_per_acre': self.quantity_kg_per_acre,
            'total_quantity_kg': self.total_quantity_kg,
            'application_stage': self.application_stage,
            'cost_estimate': self.cost_estimate,
            'safety_notes': self.safety_notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self):
        return f"<FertilizerRecommendation id={self.id} fertilizer='{self.recommended_fertilizer}'>"


class FertilizerApplication(db.Model):
    """Log of applied fertilizer events on field plots."""
    __tablename__ = 'fertilizer_applications'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    fertilizer_id = db.Column(db.Integer, db.ForeignKey('fertilizers.id', ondelete='RESTRICT'), nullable=False)
    applied_quantity_kg = db.Column(db.Float, nullable=False)
    application_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    application_method = db.Column(db.String(50), default='Broadcasting') # Broadcasting, Banding, Foliar, Fertigation
    operator_notes = db.Column(db.Text, nullable=True)

    field = db.relationship('Field', backref=db.backref('fertilizer_applications', lazy='dynamic', cascade='all, delete-orphan'))
    fertilizer = db.relationship('Fertilizer')

    def to_dict(self):
        return {
            'id': self.id,
            'field_id': self.field_id,
            'fertilizer_id': self.fertilizer_id,
            'fertilizer_name': self.fertilizer.name if self.fertilizer else 'Unknown',
            'applied_quantity_kg': self.applied_quantity_kg,
            'application_date': self.application_date.strftime('%Y-%m-%d'),
            'application_method': self.application_method,
            'operator_notes': self.operator_notes
        }


class FertilizerPurchase(db.Model):
    """Purchase invoice log for fertilizer acquisition."""
    __tablename__ = 'fertilizer_purchases'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    fertilizer_id = db.Column(db.Integer, db.ForeignKey('fertilizers.id', ondelete='RESTRICT'), nullable=False)
    bags_bought = db.Column(db.Integer, nullable=False, default=1)
    weight_per_bag_kg = db.Column(db.Float, default=50.0)
    total_cost = db.Column(db.Float, nullable=False)
    vendor_store = db.Column(db.String(100), nullable=True)
    purchase_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    farmer = db.relationship('Farmer', backref=db.backref('fertilizer_purchases', lazy='dynamic', cascade='all, delete-orphan'))
    fertilizer = db.relationship('Fertilizer')

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'fertilizer_id': self.fertilizer_id,
            'fertilizer_name': self.fertilizer.name if self.fertilizer else 'Unknown',
            'bags_bought': self.bags_bought,
            'weight_per_bag_kg': self.weight_per_bag_kg,
            'total_cost': self.total_cost,
            'vendor_store': self.vendor_store,
            'purchase_date': self.purchase_date.strftime('%Y-%m-%d')
        }

