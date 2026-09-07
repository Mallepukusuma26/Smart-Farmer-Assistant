from datetime import datetime
from app.extensions import db

class Fertilizer(db.Model):
    """Fertilizer catalog entity with N-P-K nutrient composition."""
    __tablename__ = 'fertilizers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), default='Chemical') # Nitrogenous, Phosphatic, Potassic, Complex, Organic
    n_percent = db.Column(db.Float, default=0.0)
    p_percent = db.Column(db.Float, default=0.0)
    k_percent = db.Column(db.Float, default=0.0)
    suitable_crops = db.Column(db.String(255), default='All Crops')
    application_notes = db.Column(db.Text, nullable=True)
    price_per_kg = db.Column(db.Float, default=25.0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'n_percent': self.n_percent,
            'p_percent': self.p_percent,
            'k_percent': self.k_percent,
            'npk_ratio': f"{self.n_percent}-{self.p_percent}-{self.k_percent}",
            'suitable_crops': self.suitable_crops,
            'application_notes': self.application_notes,
            'price_per_kg': self.price_per_kg
        }

    def __repr__(self):
        return f"<Fertilizer id={self.id} name='{self.name}'>"


class FertilizerRecommendation(db.Model):
    """Calculated fertilizer recommendation for a specific field/crop."""
    __tablename__ = 'fertilizer_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
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
